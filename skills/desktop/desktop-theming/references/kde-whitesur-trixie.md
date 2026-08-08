# KDE + WhiteSur on Debian 13 (trixie) — macOS clone (validated recipe)

## Why KDE over XFCE for this user
XFCE hits a hard ceiling: no real compositor blur, Global Menu is a plugin, Plank
never looks 100% native. KDE Plasma + KWin gives genuine blur (the #1 thing that
sells the macOS look) and a dock that can be a Plasma Panel with icons-only + blur.

## Valid package names on trixie (VERIFY before big install)
| Wanted | trixie name | Note |
|---|---|---|
| KDE desktop | `kde-plasma-desktop` | metapackage, pulls kwin/plasma-workspace |
| Kvantum engine | `qt-style-kvantum` + `qt-style-kvantum-themes` | binary = `kvantummanager` |
| Breeze GTK (so GTK apps match) | `breeze-gtk-theme` | |
| Login manager | `sddm` | LightDM already present; both coexist, pick session at login |
| Latte Dock | **gone** | removed upstream; DO NOT list it or apt aborts the whole install |
| Sierra window decoration | **gone** | use WhiteSur-kde aurorae (in repo) or stock Breeze |

### APT silent-abort rule
If ANY name in `apt-get install a b c` is missing, apt errors and installs NOTHING.
Always `apt-cache policy <pkg>` / `apt-cache search <kw>` first. Symptom of a bad
run: `E: Unable to locate package latte-dock` AND `dpkg -l | grep plasma` shows 0.

## Install (frontend noninteractive to avoid the debconf trap)
```bash
# pre-answer the DM prompt so a background run never blocks on debconf:
echo 'sddm sddm/default-display-manager select /usr/sbin/sddm' | sudo debconf-set-selections
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
  kde-plasma-desktop qt-style-kvantum qt-style-kvantum-themes breeze-gtk-theme sddm
```
Large download (~1.9 GB cached). If you ran it WITHOUT the noninteractive guard and
it got stuck, see "DEBCONF TRAP" below. Validate with `which plasmashell kwin_x11
sddm kvantummanager` and `dpkg -l | grep -cE '^ii.*plasma'`.

## Set the display manager to sddm (lightdm stays as fallback)
```bash
sudo ln -sf /lib/systemd/system/sddm.service /etc/systemd/system/display-manager.service
sudo systemctl enable sddm
# user picks "Plasma" vs "XFCE" at the sddm login screen
```

## Apply WhiteSur KDE  (FLAG PITFALL — KDE installer != GTK installer)
The KDE `install.sh` does NOT accept `-t`/`-o` (that's the GTK theme's syntax).
`--help` only knows `-c|--color [light|alt|dark]`, `-w|--window`, `-n|--name`.
```bash
cd /tmp && curl -sL -o w.tar.gz https://github.com/vinceliuice/WhiteSur-kde/archive/refs/heads/master.tar.gz
python3 -c "import tarfile; tarfile.open('w.tar.gz').extractall('ws')"
cd ws/WhiteSur-kde-master
./install.sh -c dark          # CORRECT — installs look-and-feel + aurorae + Kvantum
# WRONG: ./install.sh -t all -c dark  -> "ERROR: Unrecognized installation option '-t'"
```
Verify installed: `~/.local/share/plasma/look-and-feel/com.github.vinceliuice.WhiteSur-dark`,
`~/.local/share/aurorae/themes/WhiteSur-dark`, `~/.config/Kvantum/WhiteSur`.

## Apply WhiteSur GTK theme (separate repo; THIS one accepts -t all)
```bash
cd /tmp && curl -sL -o g.tar.gz https://github.com/vinceliuice/WhiteSur-gtk-theme/archive/refs/heads/master.tar.gz
python3 -c "import tarfile; tarfile.open('g.tar.gz').extractall('wg')"
cd wg/WhiteSur-gtk-theme-master
./install.sh -t all -c dark        # CORRECT for the GTK installer
# then point GTK at it:
mkdir -p ~/.config/gtk-3.0
cat > ~/.config/gtk-3.0/settings.ini <<'EOF'
[Settings]
gtk-modules=appmenu-gtk-module
gtk-theme-name=WhiteSur-Dark
gtk-icon-theme-name=WhiteSur-Dark
gtk-font-name=SF Pro Text 11
gtk-decoration-layout=close,minimize,maximize:
EOF
```

## Pre-apply configs EVEN WHEN PLASMA ISN'T RUNNING YET
Write the KDE config files directly (read at next login, idempotent). These make the
theme/blur/decor land immediately on first Plasma login without manual clicking:
```ini
# ~/.config/kdeglobals
[General]
ColorScheme=WhiteSur-dark
Name=WhiteSur-dark
widgetStyle=Kvantum
[KDE]
ColorScheme=WhiteSur-dark
LookAndFeelPackage=com.github.vinceliuice.WhiteSur-dark
widgetStyle=Kvantum
```
```ini
# ~/.config/kwinrc  (blur ON; Breeze native decoration + WhiteSur colorscheme)
# NOTE: do NOT use the aurorae WhiteSur themes on Wayland — they render the
# traffic-light buttons out of scale / off-window in Plasma 6. Use stock Breeze;
# the WhiteSur-dark colorscheme (in ~/.local/share/color-schemes) tints the
# buttons light / macOS-style and they sit correctly inside the titlebar.
[org.kde.kdecoration2]
BorderSize=Normal
# (no library=aurorae / theme=__aurorae__svg__ line — let Breeze be default)
[Compositing]
Enabled=true
[Effect-Blur]
BlurStrength=12
enabled=true
[Plugins]
blurEnabled=true
```
```ini
# ~/.config/Kvantum/kvantum.kvconfig
[General]
theme=WhiteSur
```

## Dock without Latte -> Plasma Panel as dock (configured at first Plasma login)
Ship a helper the user runs inside Plasma (e.g. `~/setup-macos-dock.sh`):
```bash
#!/bin/bash
export DISPLAY=:0.0
lookandfeeltool -a com.github.vinceliuice.WhiteSur-dark 2>/dev/null || true
kwriteconfig6 --file kwinrc --group Plugins --key blurEnabled true
kwriteconfig6 --file kwinrc --group Effect-Blur --key enabled true
kwriteconfig6 --file kvantum.kvconfig --group General --key theme WhiteSur
kwin --replace &>/dev/null &
echo "Now right-click bottom panel -> Edit Panel -> 'Icons only' + center + blur."
```
Manual dock steps if needed: right-click desktop -> Edit Mode; add Empty Panel at
bottom center; Layer=Always Visible; Visibility=Auto-Hide/Dodge; enable Blur (KWin
native); remove default widgets; add "Icons-only Task Manager" + launcher. Top panel:
native Global Menu widget (no plugin needed in KDE) + Application Launcher with an
Apple/WhiteSur icon.

## Fonts (same as XFCE path)
- SF Pro real: github.com/sahibjotsaggu/San-Francisco-Pro-Fonts ->
  /usr/share/fonts/opentype/sfpro, set as system font.
- Mono: fonts-jetbrains-mono (apt) ~ SF Mono, for Konsole.

## DEBCONF TRAP (if a background apt install got stuck on sddm.postinst)
Symptom: `ps` shows `perl /usr/share/debconf/frontend .../sddm.postinst`; `fuser
/var/lib/dpkg/lock-frontend` = LOCKED; later apt calls block. The postinst waits for
the "which display manager?" debconf prompt that never arrives headless.
FIX (do NOT issue a chained `pkill -9 -f "apt-get install"` — the user blocked that):
1. `process(action='kill')` on the stuck background job's session_id (scoped, clean).
2. `sudo DEBIAN_FRONTEND=noninteractive dpkg --configure -a`  -> DPKG_EXIT=0.
3. Then set the DM as above.

## WAYLAND: the agent shell cannot drive the user's Plasma session
Plasma 6 on trixie boots **Wayland** (kwin_wayland), not X11. The agent's terminal runs
outside the graphical session, so any attempt to run Plasma tools from it FAILS:
- `plasmashell --replace` / `kwin --replace` → `qt.qpa.plugin: Could not load the Qt
  platform plugin "xcb"` or `could not connect to display :0.0`. The agent shell lacks
  `$WAYLAND_DISPLAY` and the correct `$DISPLAY` (the user's seat was `:0`, not `:0.0`),
  and is missing `libxcb-cursor0` for the xcb plugin.
- `plasma-apply-lookandfeel` / `plasma-apply-icon-theme` / `lookandfeeltool` → same
  "cannot open display" failure.
PATTERN THAT WORKS: write the config files directly (kdeglobals / kwinrc / plasmashellrc
/ appletsrc). They are read at next login and are idempotent. Then either (a) ask the
user to **logout/login** (most reliable on Wayland), or (b) ship a helper script the
USER runs inside Plasma (Konsole) that calls `plasma-apply-*` / `kwin --replace` — those
succeed because they run in the graphical context. Do not loop re-running them from the
agent shell; it will never connect. To stop a stuck tracked job, use
`process(action='kill')` on its session_id — never a sweeping `pkill`.

## Dock won't stay visible → `panelVisibility` in plasmashellrc (NOT appletsrc)
`hideMethod` in appletsrc is IGNORED. The real control is `panelVisibility` under
`[PlasmaViews][Panel N]` in `~/.config/plasmashellrc`:
  `panelVisibility=0` Always Visible · `1` Auto Hide · `2` Windows Can Cover · `3` Windows Go Below
A dock that keeps hiding is almost always `panelVisibility=2`. Worse: orphan Panel
entries pile up across sessions (Panel 2,4,29,53,55,80,82,…) and the live dock may be
bound to one of those orphans, so editing only the "expected" Panel N does nothing.
ROBUST FIX: rewrite plasmashellrc containing ONLY the two real panels (menu + dock),
both `panelVisibility=0`, dropping every orphan ID; logout/login. If it STILL hides,
use the UI (100% reliable): right-click dock → Configure → Visibility → "Always Visible".
Also move panels via `location=` in appletsrc: `0`=top, `3`=bottom, `4`=left (the
WhiteSur installer put the dock on the LEFT as location=4 — flip it to 3 for bottom).

## Validate
- Screenshot AND show the USER (they are the final judge; vision pass is not proof).
  In one session the vision model read a themed XFCE as "a real macOS" while the
  user said it was ugly. Always confirm with the user before declaring done.
- Honest limit: without Latte Dock the dock is a Plasma Panel (icons-only + blur) —
  reads as macOS, but not pixel-identical to Big Sur's Latte.
