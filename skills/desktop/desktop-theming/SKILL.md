---
name: desktop-theming
description: Make a Linux desktop (XFCE/GNOME/KDE) look like macOS or otherwise "rice" it — WhiteSur GTK/icon/cursor themes, Plank dock, San-Francisco-like fonts, xfconf config. Use when a user asks for a macOS-style / Windows-style / themed / prettier desktop on Linux, or wants to customize their DE's look.
---

# Desktop theming / ricing on Linux (macOS look via WhiteSur)

Best, lowest-effort path to a macOS-like desktop on a GTK-based DE (XFCE, GNOME,
Cinnamon, MATE, Budgie) is the **WhiteSur** family by vinceliuice. It ships a GTK
theme, an icon set, and a cursor set that mimic Big Sur / Monterey.

## When to use
- "Deixa meu Debian/Ubuntu com cara de macOS"
- "Quero trocar o tema do XFCE/GNOME"
- Custom cursors, dock estilo Mac, top bar com relógio centralizado

## Detect the environment first
Run these before installing anything:
```
echo "XDG_CURRENT_DESKTOP=$XDG_CURRENT_DESKTOP"
cat /etc/X11/default-display-manager 2>/dev/null
ls /usr/share/xsessions/
dpkg -l | grep -Ei 'xfce4|gnome-shell|plasma|cinnamon' | awk '{print $2}'
```
WhiteSur targets GTK DEs. On XFCE it is a near-perfect macOS clone; on KDE use a
different approach (not covered here).

## Install dependencies
```
sudo apt-get install -y git curl wget sassc inkscape plank fonts-inter x11-apps
```
NOTE: on Debian `xcursorgen` is NOT a separate package — it lives inside `x11-apps`.
Installing `xcursorgen` by name fails with "no candidate"; just install `x11-apps`.

## Clone the THREE separate repos (critical pitfall)
The cursor theme is a **separate repository**. The gtk-theme repo does NOT contain
cursors, and its `install.sh` will silently do nothing useful if you point it at the
cursor job. Clone each independently:
```
mkdir -p ~/.themes-src && cd ~/.themes-src
git clone --depth 1 https://github.com/vinceliuice/WhiteSur-gtk-theme.git
git clone --depth 1 https://github.com/vinceliuice/WhiteSur-icon-theme.git
git clone --depth 1 https://github.com/vinceliuice/WhiteSur-cursors.git
```
Do NOT clone the same URL three times into differently-named dirs — the loop
`git clone <gtk-url> WhiteSur-cursors` produces a cursor dir that is actually the
GTK theme (detected by `git remote -v` showing the gtk URL). If `install.sh` in the
"cursor" dir prints the GTK banner, you cloned the wrong repo — `rm -rf` and re-clone
the real `WhiteSur-cursors` URL.

## Install the themes (flag pitfall)
The installer flags changed over time. Current valid form (verify with `./install.sh --help`):
```
# GTK theme (sudo -> /usr/share/themes)
cd ~/.themes-src/WhiteSur-gtk-theme
sudo ./install.sh --dest /usr/share/themes -c dark -c light -o normal -o solid -t blue
# libadwaita / GTK4 (MUST NOT run with sudo -> installs to ~/.themes)
./install.sh -l -c dark -c light -t blue
```
- `--color all` and `--size 220` are REJECTED by current versions ("Unrecognized
  variant/option"). Use `-c dark -c light` (repeatable).
- `--libadwaita` / `-l` writes to `~/.themes` and the script explicitly warns
  "Do not run '--libadwaita' option with sudo!" — run as the normal user.
```
# Icons (sudo -> /usr/share/icons)
sudo ~/.themes-src/WhiteSur-icon-theme/install.sh --dest /usr/share/icons --theme all
# Cursors (user -> ~/.local/share/icons/WhiteSur-cursors)
~/.themes-src/WhiteSur-cursors/install.sh
```

## Apply on XFCE — the offline-robust way
`xfconf-query` only works inside a running graphical session (needs `xfconfd` on the
per-session DBus). When scripting from a headless/SSH context, **edit the XML files
directly** — they are read at next login and are idempotent. Location:
`~/.config/xfce4/xfconf/xfce-perchannel-xml/*.xml`

Key properties to set:
- `xsettings.xml`: `Net/ThemeName`=WhiteSur-Dark, `Net/IconThemeName`=WhiteSur-Dark,
  `Gtk/CursorThemeName`=WhiteSur-cursors, `Gtk/FontName`="SF Pro Text 11"  # real SF Pro preferred (see "San Francisco fonts" below); Inter 10 is fallback
  `Xft/Antialias`=1, `Xft/Hinting`=1, `Xft/HintStyle`="hintslight", `Xft/RGBA`="rgb",
  `Gtk/DecorationLayout`="close,minimize,maximize:menu" (Mac: buttons LEFT).
- `xfwm4.xml`: `general/theme`=WhiteSur-Dark, `general/button_layout`="HMC"
 (Hide/min, Max, Close all on the LEFT — Mac traffic-light order; `|` separates left/right groups if any stay on the right),
  `general/use_compositing`=true (needed for shadows/transparency).
- `xfce4-desktop.xml`: set `last-image` / `image-path` / `image-show` on each monitor
  to the wallpaper path (e.g. the repo's
  `src/assets/gnome-shell/backgrounds/background-default.png` copied to ~/Pictures).
- `xfce4-panel.xml`: top bar = panel with `applicationsmenu` (set
  `show-button-title`=false, `button-icon`="distributor-logo" for an Apple-like menu),
  an expanding `separator`, then `clock` (mode 2, format "%a %d %b  %H:%M") centered
  between two expanding separators. Remove the bottom launcher panel so it doesn't
  clash with the Plank dock.

After editing XMLs, also ship a `apply-whitesur.sh` that re-applies everything via
`xfconf-query` for use when the user is already logged in (so changes take effect
live without a full logout). See references/whitesur-xfce-recipe.md.

## Dock (Plank)
```
mkdir -p ~/.local/share/plank/themes
cp -r ~/.themes-src/WhiteSur-gtk-theme/other/plank/theme-Dark ~/.local/share/plank/themes/WhiteSur-Dark
mkdir -p ~/.config/plank/dock1
# write a [PlankDockPreferences] settings file: Position=3 (bottom), HorizonAlignment=center,
# ZoomEnabled=true, ZoomPercent=150, IconSize=48, HideMode=1, Theme=WhiteSur-Dark
# autostart:
cat > ~/.config/autostart/plank.desktop <<'EOF'
[Desktop Entry]
Type=Application
Exec=plank
X-XFCE-Autostart-enabled=true
EOF
```
Users pin apps by right-clicking a running app's dock icon → "Keep in Dock".

## San Francisco fonts (real SF Pro, not just Inter)
Inter is only an SF *substitute*. For pixel fidelity install the actual SF Pro:
```bash
cd /tmp
curl -sL -o sfpro.zip "https://github.com/sahibjotsaggu/San-Francisco-Pro-Fonts/archive/refs/heads/master.zip"
python3 -c "import zipfile; zipfile.ZipFile('sfpro.zip').extractall('sftmp')"
sudo mkdir -p /usr/share/fonts/opentype/sfpro
find sftmp \( -iname '*.otf' -o -iname '*.ttf' \) -exec sudo cp {} /usr/share/fonts/opentype/sfpro/ \;
sudo fc-cache -f /usr/share/fonts/opentype/sfpro
```
Then set `Gtk/FontName`="SF Pro Text 11". For the terminal, use an SF-Mono-like mono
— `fonts-jetbrains-mono` (apt) is very close to SF Mono.

## Global Menu (the macOS top-bar app menu — sells the look)
Gets the app's menu to rise into the top panel like macOS:
```bash
sudo apt-get install -y xfce4-appmenu-plugin appmenu-gtk3-module appmenu-gtk-module-common
xfconf-query -c xfce4-panel -p /plugins/plugin-10 -t string -s appmenu --create
xfconf-query -c xfce4-panel -p /plugins/plugin-10/expand -t bool -s true
mkdir -p ~/.config/gtk-3.0
printf '[Settings]\ngtk-modules=appmenu-gtk-module\n' > ~/.config/gtk-3.0/settings.ini
echo 'export UBUNTU_MENUPROXY=1' >> ~/.profile
xfce4-panel --restart   # required for the plugin to appear
```

## Apple menu icon
Replace `distributor-logo` with an Apple glyph so the top-left reads as macOS:
- Save a filled `#f5f5f7` apple SVG; `sudo convert -background none apple.svg -resize 24x24 /usr/share/pixmaps/apple-menu.png` (needs `imagemagick` / `convert`).
- `xfconf-query -c xfce4-panel -p /plugins/plugin-1/button-icon -s /usr/share/pixmaps/apple-menu.png`
  and `/plugins/plugin-1/show-button-title -s false`.

## Window shadows + APPLY (easy to skip)
Compositing alone is not enough — set the shadow params AND restart xfwm4 or they
won't paint (a common "why are there no shadows" miss):
```bash
xfconf-query -c xfwm4 -p /general/use_compositing -s true
xfconf-query -c xfwm4 -p /general/show_frame_shadow -s true
xfconf-query -c xfwm4 -p /general/show_dock_shadow -s true
xfconf-query -c xfwm4 -p /general/shadow_opacity -s 65
xfconf-query -c xfwm4 -p /general/shadow_delta_y -s 5
xfconf-query -c xfwm4 -p /general/shadow_delta_width -s -10
xfconf-query -c xfwm4 -p /general/shadow_delta_height -s -10
xfconf-query -c xfwm4 -p /general/button_layout -s "HMC"
xfwm4 --replace &   # MUST restart for shadows + button order to apply
```

## Validate before declaring done
```
python3 -c "import xml.dom.minidom as m; [m.parse(f'$HOME/.config/xfce4/xfconf/xfce-perchannel-xml/{x}.xml') for x in ('xsettings','xfwm4','xfce4-panel','xfce4-desktop')]; print('XML OK')"
[ -d /usr/share/themes/WhiteSur-Dark ] && echo "gtk ok"
[ -d /usr/share/icons/WhiteSur-Dark ] && echo "icons ok"
[ -d ~/.local/share/icons/WhiteSur-cursors ] && echo "cursor ok"
```

## Honest limits (tell the user)
 XFCE/Plank cannot do real blur on the dock or a native Launchpad, so it reaches ~90%
 of the macOS look, not 100%. No compositor blur like a true macOS.

## KDE Plasma path (for a MORE faithful macOS clone than XFCE)
 If the user wants real blur / a true macOS dock, KDE Plasma is the better base than
 XFCE. **Debian 13 (trixie) package-name drift — CRITICAL pitfall:**
 - `latte-dock` — REMOVED from Debian (upstream unmaintained). Not installable.
 - `kvantum-manager` — renamed; the binary now ships in `qt-style-kvantum` (install
   `qt-style-kvantum` + `qt-style-kvantum-themes`; run `kvantummanager`).
 - `kwin-decoration-sierra-break` — does NOT exist; use the WhiteSur KDE aurorae
   decoration (ships inside the WhiteSur-kde repo) or stock Breeze.

 **APT SILENT-ABORT pitfall:** `apt-get install -y a b c` where ANY package name is
 missing does NOT install the others — it errors and installs NOTHING (not even the
 valid packages). Always verify names with `apt-cache policy <pkg>` BEFORE the big
 install. Symptom: first attempt prints `E: Unable to locate package ...` and
 `plasma` pkg count stays 0 → re-run with only valid names.

 Working trixie install set:
 ```bash
 sudo apt-get install -y kde-plasma-desktop qt-style-kvantum qt-style-kvantum-themes \
   breeze-gtk-theme sddm
 ```

 **BACKGROUND-INSTALL DEBCONF TRAP (cost this session ~20 min):** if the above `apt-get`
 runs via `terminal(background=true)`, the `sddm.postinst` stops and waits for debconf
 input (the "which display manager?" prompt) that never arrives in a headless background
 shell. It then HOLDS the dpkg lock forever — `dpkg --configure -a` and every later apt
 call block on `/var/lib/dpkg/lock-frontend`. Symptoms: `ps` shows
 `perl /usr/share/debconf/frontend .../sddm.postinst` alive; `fuser
 /var/lib/dpkg/lock-frontend` reports LOCKED; `apt-get` prints "frontend lock was locked
 by apt-get pid …".
   FIX (do NOT reach for `pkill -9 -f "apt-get install"` — see workflow note below):
   1. Kill ONLY the stuck background install job via the tool: `process(action='kill')`
      on its session_id (clean, scoped — not a process-wide pkill).
   2. `sudo DEBIAN_FRONTEND=noninteractive dpkg --configure -a`  → finishes all pending
      packages (DPKG_EXIT=0, no debconf prompt).
   3. Set the DM: `sudo ln -sf /lib/systemd/system/sddm.service
      /etc/systemd/system/display-manager.service` and `sudo systemctl enable sddm`
      (lightdm stays installed as fallback; user picks Plasma/XFCE at login).
   If you must run the big apt install in background, pre-set the answer first:
   `echo 'sddm sddm/default-display-manager select /usr/sbin/sddm' | sudo debconf-set-selections`
   before launching, OR just run it foreground (it's ~1.9 GB; a 300 s foreground timeout
   is fine).

 **WORKFLOW NOTE (user-corrected):** when an apt/dpkg process is stuck, do NOT issue a
 chained `pkill -9 -f "apt-get install"` / `pkill -9 -f debconf` — the user BLOCKED that
 exact command mid-session ("BLOCKED: User denied this action"). Use the Hermes
 `process(action='kill')` tool on the specific background session_id instead. It is the
 sanctioned way to terminate a tracked background job without a sweeping system-wide kill.
 Apply WhiteSur KDE (global + Kvantum + aurorae + plasma) via the repo's `install.sh`
 (`https://github.com/vinceliuice/WhiteSur-kde`). **FLAG PITFALL:** the KDE installer does
 NOT accept the GTK-style `-t` / `-o` flags — `./install.sh -t all -c dark` prints
 `ERROR: Unrecognized installation option '-t'` and exits 1. The KDE `install.sh --help`
 only knows `-c|--color [light|alt|dark]`, `-w|--window`, `-n|--name`. Correct form:
 ```bash
 cd WhiteSur-kde-master && ./install.sh -c dark      # installs look-and-feel + aurorae + Kvantum
 ```
 (The GTK theme is a SEPARATE repo — `WhiteSur-gtk-theme` — run its `./install.sh -t all -c dark`
 there; that one DOES accept `-t all`. Don't cross-contaminate the two installers.)
 Since Latte Dock is gone, configure the **Plasma Panel as a bottom dock** (icons-only,
 auto-hide, blur on) — reads as macOS dock with real KWin blur. See
 `references/kde-whitesur-trixie.md`.

 LightDM already in control → selecting Plasma at login is safe; do NOT remove XFCE
 (user keeps both, picks at login).

 **WAYLAND: the agent's shell CANNOT drive the user's session.** Plasma 6 on trixie
 defaults to **Wayland** (kwin_wayland), not X11. The agent's terminal runs OUTSIDE
 the graphical session, so every attempt to manage Plasma from the agent shell FAILS:
 - `plasmashell --replace` / `kwin --replace` error with `qt.qpa.plugin: Could not load
   the Qt platform plugin "xcb"` or `could not connect to display :0.0` — because the
   agent shell has no `$WAYLAND_DISPLAY`/correct `$DISPLAY` and lacks `libxcb-cursor0`
   for the xcb plugin. (DISPLAY on the user's seat was `:0`, NOT `:0.0`.)
 - `plasma-apply-lookandfeel` / `plasma-apply-icon-theme` / `lookandfeeltool` similarly
   cannot open the display from the agent shell.
 CORRECT PATTERN: write the KDE config files directly (kdeglobals, kwinrc, plasmashellrc,
 appletsrc) — they are read at next login / when the user restarts Plasma. Then either
 (a) tell the user to **logout/login** (most reliable on Wayland), or (b) ship a helper
 script the USER runs inside their Plasma session (Konsole) that calls the
 `plasma-apply-*` / `kwin --replace` commands — those work because they run in the
 graphical context. Do NOT loop trying to run them from the agent shell; it will never
 connect. If you must poke a running process, use `process(action='kill')` on the
 background session_id, never a sweeping `pkill`.

 **WINDOW BUTTONS "out of scale" on Wayland → use Breeze, not aurorae.** The WhiteSur
 aurorae themes (`__aurorae__svg__WhiteSur-dark` / `WhiteSurLiquid-dark`) mal-position
 the traffic-light buttons in Plasma 6 / Wayland (buttons render huge / outside the
 titlebar / off-window). This was reproducible across two aurorae variants and did NOT
 fix with `BorderSize=Tiny`. WORKING FIX: set the window decoration to **stock Breeze**
 with the **WhiteSur-dark colorscheme** — Breeze is the native KDE decoration, renders
 perfectly on Wayland, and the WhiteSur colorscheme tints the buttons light/macOS-style.
 In kwinrc do NOT set `library=org.kde.kwin.aurorae`; use the Breeze default (leave the
 aurorae line out or set `theme=Breeze`). The colorscheme (already in
 `~/.local/share/color-schemes/WhiteSur-dark.colors`) carries the look.

 **RESET-FIRST RULE (user-corrected this session):** when several decoration variants fail
 and the user says "refaça do 0 / ficou horrível", STOP trying new variants and FIRST
 restore the **stock Breeze default** (working state) so the desktop is at least
 functional, THEN iterate. Concretely: write kwinrc with
 `library=org.kde.kwin.decoration` + `theme=Breeze` + `BorderSize=Normal` (no aurorae
 line), ship a `reset-clean.sh` the user runs in Konsole, and only after they confirm
 "buttons normal now" discuss re-attempting colored traffic-lights (e.g. compile
 kwin-decoration-sierra). Do not chain 3–4 failed decoration swaps — each broken state
 costs the user a restart and erodes trust.

 **`kwin --replace` inside a helper script ABORTS on Wayland.** When the user runs a
 Konsole script that ends with `kwin --replace &` it can abort (kwin_wayland is the
 compositor; re-exec from a user script is flaky). Safer: have the script NOT restart
 KWin and instead tell the user to **logout/login** to apply the new kwinrc. If a live
 restart is needed, the most reliable is `systemctl --user restart
 plasma-kwin_wayland.service` (may drop the session) — prefer logout/login.

 **DOCK WON'T STAY VISIBLE → panel visibility lives in `plasmashellrc`, not appletsrc.**
 `hideMethod` in appletsrc is ignored; the real key is `panelVisibility` under
 `[PlasmaViews][Panel N]` in `~/.config/plasmashellrc`:
   `panelVisibility=0`=Always Visible, `1`=Auto Hide, `2`=Windows Can Cover, `3`=Windows Go Below.
 A stuck auto-hide dock is almost always `panelVisibility=2`. ALSO: stale/orphan Panel
 entries accumulate in plasmashellrc across sessions (Panel 2,4,29,53,55,80,82,…) and the
 live dock may be bound to one of those orphan IDs, so editing only the "expected" Panel
 N does nothing. The robust fix is to **rewrite plasmashellrc with ONLY the two real
 panels** (menu Panel N + dock Panel M), both `panelVisibility=0`, dropping all orphan
 IDs. Reboot/login to apply. If it STILL hides, the 100%-reliable path is the UI:
 right-click dock → Configure → Visibility → "Always Visible".

**The USER is the final judge of "looks good".** An AI vision pass that says "this
looks like macOS" is NOT proof — in one session the vision model read the themed
desktop as "a real macOS" while the user said it was ugly. Always show the user a
screenshot and ask before declaring done; iterate on their specific complaints
(they usually point at the terminal font, inconsistent light/dark apps, or weak
window shadows — not the theme itself).

**MS Office 2019/365 will NOT install via Wine.** The Click-to-Run setup.exe
(Office Deployment Tool) crashes loading `msxml6.dll` (page fault) under Wine 10.
Use **OnlyOffice** (native Linux, Word-2019-identical UI, opens/saves .docx) as the
Word substitute — see `references/macos-office-word.md`. Real Office 2010/2013 MSI
ISOs DO run on Wine if the user insists on genuine Office.

## Reference
 - `references/whitesur-xfce-recipe.md` — full copy-paste recipe incl. the apply script.
 - `references/macos-office-word.md` — install OnlyOffice (Word substitute) + why Office 2019/365 C2R fails on Wine.
 - `references/kde-whitesur-trixie.md` — KDE/WhiteSur on Debian 13: valid pkg names, dock-as-panel, apply steps.
