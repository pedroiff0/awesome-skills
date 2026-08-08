# macOS-look desktop: installing a Word substitute (Office on Linux)

## TL;DR
- MS **Office 2019 / 365 via Wine = does NOT work.** The Click-to-Run (C2R)
  `setup.exe` from the Office Deployment Tool crashes under Wine 10 with a page
  fault while loading `msxml6.dll` (`err:ole:apartment_add_dll couldn't load
  in-process dll ... msxml6.dll`, then `wine: Unhandled page fault`, `SETUP_EXIT=5`).
  This is a known incompatibility, not a missing dependency — installing
  `winetricks msxml6 corefonts` does NOT fix it.
- Use **OnlyOffice Desktop Editors** as the Word substitute: native Linux, UI is
  near-identical to MS Word 2019/365, opens/edits/saves `.docx` perfectly.

## Install OnlyOffice (preferred)
Download the official .deb directly (the GPG-key-in-repo path is flaky behind
proxies / on trixie):
```bash
cd /tmp
curl -sL -o onlyoffice.deb \
  "https://download.onlyoffice.com/install/desktop/editors/linux/onlyoffice-desktopeditors_amd64.deb"
sudo apt-get install -y ./onlyoffice.deb   # ~350 MB, pulls gtk/qt deps
# binary: /usr/bin/onlyoffice-desktopeditors
```
Launch with `DISPLAY=:0.0 onlyoffice-desktopeditors &` (harmless Gtk/QXcb warnings).

## If the user insists on genuine Office via Wine
Only the **MSI-based** editions run well (Wine AppDB: Gold/Platinum):
- Office **2010 / 2013** volume ISO (MSI, not C2R). Mount, run `setup.exe` in a
  64-bit prefix. Requires `wine32` (Debian trixie: `sudo dpkg --add-architecture
  i386 && sudo apt-get install wine32`) or the prefix corrupts with
  `c0000135` (kernel32.dll fails to load). Recreate the prefix from scratch if it
  got into that state: `rm -rf ~/.wine && WINEPREFIX=~/.wine WINEARCH=win64 wineboot --init`.
- Office **2019 / 365 (C2R)** = avoid. The ODT `setup.exe` is 32-bit and crashes
  on msxml6 under Wine 10. No reliable workaround found.

## Notes from a real session (pedro, Debian 13 trixie, XFCE + Wine 10)
- `OfficeSetup.exe` in ~/Downloads was the M365 streaming installer — also fails
  on Wine (ShellExecuteEx internal error / page fault). Same root cause as C2R.
- After a failed Wine prefix, `wine` itself broke (`could not load kernel32.dll,
  status c0000135`). Fix = delete `~/.wine` and re-init with wine32 present.
- Decision flow that worked: asked the user, they chose "OnlyOffice (native,
  identical to Word 2019) — resolves today" over fighting Wine.
