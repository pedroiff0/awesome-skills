# WhiteSur on XFCE — full recipe

Target: Debian 13 (trixie) + XFCE4 + LightDM + NVIDIA. Verified working 2026-08-02.

## 1. Dependencies
```
sudo apt-get update
sudo apt-get install -y git curl wget sassc inkscape plank fonts-inter x11-apps
# NOTE: xcursorgen is inside x11-apps on Debian; no separate package.
```

## 2. Clone (3 SEPARATE repos!)
```
mkdir -p ~/.themes-src && cd ~/.themes-src
git clone --depth 1 https://github.com/vinceliuice/WhiteSur-gtk-theme.git
git clone --depth 1 https://github.com/vinceliuice/WhiteSur-icon-theme.git
git clone --depth 1 https://github.com/vinceliuice/WhiteSur-cursors.git
# Verify remotes differ:
git -C WhiteSur-cursors remote -v   # must show WhiteSur-cursors.git
```

## 3. Install
```
# GTK (system):
sudo ~/.themes-src/WhiteSur-gtk-theme/install.sh --dest /usr/share/themes -c dark -c light -o normal -o solid -t blue
# libadwaita/GTK4 (user, NO sudo):
~/.themes-src/WhiteSur-gtk-theme/install.sh -l -c dark -c light -t blue
# Icons (system):
sudo ~/.themes-src/WhiteSur-icon-theme/install.sh --dest /usr/share/icons --theme all
# Cursors (user):
~/.themes-src/WhiteSur-cursors/install.sh
```
Current installer flags: `-c dark -c light`, `-o normal -o solid`, `-t blue`.
REJECTED (old): `--color all`, `--size 220`.

## 4. Wallpaper
```
cp ~/.themes-src/WhiteSur-gtk-theme/src/assets/gnome-shell/backgrounds/background-default.png ~/Pictures/WhiteSur-BigSur.png
```

## 5. apply-whitesur.sh (run WHILE LOGGED IN to apply live)
Save as ~/apply-whitesur.sh and `chmod +x`:
```bash
#!/usr/bin/env bash
set -e
THEME=WhiteSur-Dark; ICONS=WhiteSur-Dark; CURSOR=WhiteSur-cursors
xfconf-query -c xsettings -p /Net/ThemeName -s $THEME 2>/dev/null || true
xfconf-query -c xsettings -p /Net/IconThemeName -s $ICONS 2>/dev/null || true
xfconf-query -c xsettings -p /Gtk/CursorThemeName -s $CURSOR 2>/dev/null || true
xfconf-query -c xsettings -p /Gtk/CursorThemeSize -s 24 2>/dev/null || true
xfconf-query -c xsettings -p /Gtk/FontName -s "Inter 10" 2>/dev/null || true
xfconf-query -c xsettings -p /Xft/Antialias -s 1 2>/dev/null || true
xfconf-query -c xsettings -p /Xft/Hinting -s 1 2>/dev/null || true
xfconf-query -c xsettings -p /Xft/HintStyle -s hintslight 2>/dev/null || true
xfconf-query -c xsettings -p /Xft/RGBA -s rgb 2>/dev/null || true
xfconf-query -c xsettings -p /Gtk/DecorationLayout -s "close,minimize,maximize:menu" 2>/dev/null || true
xfconf-query -c xfwm4 -p /general/theme -s $THEME 2>/dev/null || true
xfconf-query -c xfwm4 -p /general/button_layout -s "CHM|" 2>/dev/null || true
xfconf-query -c xfwm4 -p /general/use_compositing -s true 2>/dev/null || true
# Plank + wallpaper as described in SKILL.md
```

## 6. Gotchas
- `xfconf-query` needs the session DBus. From SSH/headless, edit the XMLs directly
  (they load at next login). Both paths were set in the real session.
- Verify XML validity with `python3 -c "import xml.dom.minidom as m; m.parse(path)"`.
- If the cursor dir is empty after install, re-check you cloned WhiteSur-cursors (not gtk-theme).
