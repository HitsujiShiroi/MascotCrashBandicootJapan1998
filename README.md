# Crash Bandicoot Desktop Character JAPAN (1998) — Remastered Edition
**マスコット・クラッシュ・バンディクー (1998)**

A faithful, modern cross-platform recreation and archival preservation of the **1998 Japan-exclusive PC desktop mascot** originally developed by **SME Intermedia Inc. / flagship inc.** for Windows 95/98, rebuilt in Python + PySide6 for **Windows 10/11, macOS, and Linux**.

---

## Features

### Phase 1: Interactive Desktop Mascot
- **202 Original Sprites Preserved:** Pixel-accurate transparent frames extracted from the original 1998 Japanese release, including native left/right directional animations (*Walk, Run, Jump, Cyclone Spin, Crash Landing, and Idle*).
- **Desktop Physics & Gravity:** Crash walks, dashes, spins, and jumps across your screen, landing on your taskbar and active windows (Windows).
- **Japanese Audio Jukebox:** Includes the official 1998 Japanese theme **「クラッシュ万事休す」 (*Crash Banji Kyūsu*)** with volume controls, quick-mute, and playback transport.
- **Modern Quality-of-Life:**
  - **Multi-Crash Clones:** Spawn as many Crashes as you want on screen.
  - **Display Controls:** 1x to 4x pixel-art scaling, opacity slider, and multi-monitor support.
  - **Gaming & Productivity Friendly:** Auto-hide in fullscreen apps/games, Ghost Mode (click-through), Lock Position, and Rescue Hotkey (`Ctrl + Shift + C` or double-click the system tray icon).
  - **Multi-Language & Custom Packs:** Built-in support for 10 languages and external `characters/` packs.

### Phase 2: 1998 CD-ROM Extras & Historical Gallery
Accessible anytime from the right-click menu (**Extras & Gallery (1998)...**) or Options:
- **Original Wallpapers (1998):** All 6 classic wallpapers across their original resolutions (up to `1280x1024`), with one-click **Set as Desktop Wallpaper** (Windows, macOS, Linux) and export.
- **20 Classic Desktop Icons (`.ico`):** Preview and export the complete 1998 Windows 95 icon pack (*Crash, Aku Aku, Polar, Cortex, Crates, Wumpa Fruit, etc.*).
- **Historical Gallery:** Physical manual and CD scans, 12 move cards, *Crash Theater* & *Characters File* screensaver sheets, and Win95 Startup/Shutdown screen archive.
- **MACS Animations (`.avi`):** All 6 original flagship Inc. resident window animations (`mgn_start.avi` to `mgn_end.avi`).
- **Screensaver Voices & SFX (`.wav`):** Built-in player for the 16 original Japanese screensaver voice clips and sound effects.

---

## Download & Installation

Download the standalone package for your operating system from the [**Releases**](https://github.com/HitsujiShiroi/MascotCrashBandicootJapan1998/releases) page:

- **Windows 10/11:** Extract `MascotCrashBandicootJapan1998-Windows.zip` and run `MascotCrashBandicootJapan1998.exe`.
- **macOS:** Extract `MascotCrashBandicootJapan1998-macOS.zip`. On first launch, right-click `MascotCrashBandicootJapan1998.app` → **Open** (or run `xattr -cr MascotCrashBandicootJapan1998.app` in Terminal if Gatekeeper blocks unsigned apps).
- **Linux:** Extract `MascotCrashBandicootJapan1998-Linux.tar.gz`, grant execution permissions (`chmod +x MascotCrashBandicootJapan1998`), and run `./MascotCrashBandicootJapan1998`.

---

## Running from Source

```bash
pip install PySide6
python main.py
