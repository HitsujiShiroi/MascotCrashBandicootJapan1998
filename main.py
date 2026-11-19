import sys
import os
import json
import wave
import shutil
import random
import subprocess
import ctypes

IS_WINDOWS = sys.platform == "win32"
IS_MACOS = sys.platform == "darwin"
IS_LINUX = sys.platform.startswith("linux")

if IS_WINDOWS:
    from ctypes import wintypes

from PySide6.QtWidgets import (
    QApplication, QLabel, QMenu, QDialog, QVBoxLayout, QHBoxLayout,
    QCheckBox, QPushButton, QSplashScreen, QComboBox, QFormLayout,
    QSlider, QGroupBox, QTabWidget, QWidget, QSystemTrayIcon,
    QListWidget, QListWidgetItem, QFileDialog, QMessageBox, QFrame
)
from PySide6.QtCore import Qt, QTimer, QPoint, QUrl, QAbstractNativeEventFilter, QSize
from PySide6.QtGui import QPixmap, QTransform, QAction, QIcon, QActionGroup, QDesktopServices
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput, QSoundEffect
from PySide6.QtNetwork import QLocalServer, QLocalSocket


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def resolve_asset_dir(primary_rel, fallback_rel):
    p1 = resource_path(primary_rel)
    if os.path.isdir(p1) and os.listdir(p1):
        return p1
    p2 = resource_path(fallback_rel)
    if os.path.isdir(p2) and os.listdir(p2):
        return p2
    return p1


def get_config_path():
    if IS_WINDOWS:
        base = os.environ.get("APPDATA")
    elif IS_MACOS:
        base = os.path.expanduser("~/Library/Application Support")
    else:
        base = os.environ.get("XDG_CONFIG_HOME") or os.path.expanduser("~/.config")

    if base:
        cfg_dir = os.path.join(base, "CrashMascotJapan1998")
        try:
            os.makedirs(cfg_dir, exist_ok=True)
            return os.path.join(cfg_dir, "crash_jp_config.json")
        except Exception:
            pass
    return "crash_jp_config.json"


CONFIG_FILE = get_config_path()
SERVER_NAME = "CrashBandicootDesktopJapan1998_SingleInstance"
HOTKEY_RESCUE_ID = 0x1999

FALLBACK_EN = {
    "_lang_name": "English",
    "menu_start_dance": "Start Running & Actions",
    "menu_stop": "Stop (Idle)",
    "menu_bring_center": "Bring Crash to Center",
    "menu_clones": "Clones (Multi-Crash)",
    "act_spawn_clone": "➕ Spawn Another Crash",
    "act_dance_all": "🏃 All: Start Running",
    "act_stop_all": "🛑 All: Stop",
    "act_clear_clones": "🧹 Remove Extra Clones",
    "act_close_this": "Close This Crash",
    "toast_clone_spawned": "Clones active: {count}",
    "menu_character": "Character Pack",
    "menu_animations": "Actions & Moves",
    "menu_random_move": "Random Action",
    "move_walk": "Walk Patrol",
    "move_run": "Dash Run",
    "move_spin": "Cyclone Spin",
    "move_jump": "Desktop Jump",
    "move_squash": "Crash Landing",
    "menu_pos_fs": "Position && Fullscreen",
    "act_hide_fs": "Auto-Hide in Fullscreen",
    "act_force_fs": "Show Over Fullscreen",
    "act_gravity": "Enable Desktop Gravity",
    "act_lock_pos": "Lock Position",
    "act_ghost_mode": "Ghost Mode (Click-Through)",
    "menu_vol_ost": "Volume && Japanese Audio",
    "menu_quick_vol": "Quick Volume",
    "act_play_music": "▶ Play Music",
    "act_pause_music": "⏸ Pause Music",
    "act_next_track": "⏭ Next Track",
    "act_prev_track": "⏮ Previous Track",
    "act_mute_all": "Mute All",
    "act_enable_music": "Enable Music",
    "act_sfx": "Sound Effects",
    "menu_extras": "Extras && Gallery (1998)...",
    "menu_options": "Options",
    "menu_about": "About Japanese Edition",
    "menu_exit": "Bye Bye",
    "win_options_title": "Mascot Crash Bandicoot (Japan 1998) - Options",
    "win_about_title": "About Mascot Crash Bandicoot (1998 Japan)",
    "tab_classic": "General && Behavior",
    "tab_audio": "Audio && Jukebox",
    "tab_desktop": "Desktop && System",
    "tab_extras": "Extras && Gallery (1998)",
    "grp_1998": "Original 1998 Rules (SME Intermedia / flagship)",
    "cb_allow_move": "Allow Crash to run and jump across the screen",
    "cb_vary_length": "Vary length of spontaneous actions",
    "cb_continue_dancing": "Keep roaming continuously after an action",
    "grp_timing": "Speed, Activity && Language",
    "lbl_character": "Character:",
    "lbl_language": "Language:",
    "lbl_dance_speed": "Animation Speed:",
    "lbl_spontaneous": "Spontaneous Activity:",
    "spd_slow": "0.5x (Slow)",
    "spd_normal": "1.0x (Original 1998)",
    "spd_fast": "1.5x (Fast)",
    "spd_turbo": "2.0x (Turbo)",
    "idle_never": "Never (Stand Still)",
    "idle_rarely": "Rarely",
    "idle_normal": "Normal (1998)",
    "idle_hyper": "Hyperactive",
    "btn_mute_all": "Mute All Audio",
    "btn_unmute_all": "Unmute All Audio (MUTED)",
    "grp_music": "Japanese Music && Audio Jukebox",
    "cb_enable_music": "Enable Music",
    "lbl_selected_track": "Selected Track:",
    "opt_random_track": "Random Track",
    "lbl_now_playing": "Now Playing: {track}",
    "btn_prev": "⏮ Previous",
    "btn_play": "▶ Play",
    "btn_pause": "⏸ Pause",
    "btn_next": "⏭ Next",
    "cb_autoplay": "Auto-advance to next track when song ends",
    "grp_sfx": "Sound Effects (SFX)",
    "cb_enable_sfx": "Enable SFX",
    "grp_display": "Display && Multi-Monitor",
    "lbl_scale": "Sprite Scale:",
    "lbl_opacity": "Opacity:",
    "lbl_screen": "Active Screen:",
    "scale_1x": "1x (Original 1998)",
    "scale_2x": "2x (HD)",
    "scale_3x": "3x (Full HD)",
    "scale_4x": "4x (4K)",
    "lbl_monitor_item": "Monitor {num} ({w}x{h})",
    "grp_fs": "Fullscreen && Gaming Behavior",
    "cb_hide_fs": "Auto-Hide && Pause in Fullscreen / Exclusive Games",
    "cb_force_fs": "Show Over Fullscreen (Force Always-On-Top)",
    "grp_sys": "Desktop Physics, Position && Startup",
    "cb_gravity": "Enable Gravity on Desktop (Lands on windows && taskbar)",
    "cb_lock_pos": "Lock Position on Screen (Stay pinned in place)",
    "cb_splash": "Show Startup Splash Screen",
    "cb_startup": "Run Crash automatically at System Startup",
    "cb_ghost": "Ghost Mode (Mouse clicks pass through Crash)",
    "lbl_hotkey_info": "Rescue Shortcut: Ctrl + Shift + C (or Tray Double-Click)",
    "btn_reset_1998": "Reset 1998 Defaults",
    "btn_apply_ok": "Apply && OK",
    "txt_no_tracks": "No tracks found",
    "toast_now_playing": "♪ Now Playing: {track}",
    "toast_rescued": "Crash rescued to center!",
    "ext_cat_wallpapers": "Wallpapers (1998)",
    "ext_cat_icons": "Desktop Icons (.ico)",
    "ext_cat_gallery": "Gallery, Manga && Manual",
    "ext_cat_videos": "MACS Animations (.avi)",
    "ext_cat_sfx": "Screensaver Voices && SFX (.wav)",
    "ext_btn_wallpaper": "🖥 Set as Desktop Wallpaper",
    "ext_btn_save": "💾 Save / Export Selected...",
    "ext_btn_export_icons": "📦 Export All 20 Icons (.ico)",
    "ext_btn_play": "▶ Play Media",
    "ext_btn_open_folder": "📂 Open Folder",
    "ext_msg_wp_ok": "Desktop wallpaper updated successfully!",
    "ext_msg_icons_ok": "Exported {count} icons to:\n{path}"
}

DEFAULT_SETTINGS = {
    "character_id": "crash_jp_1998",
    "language": "en",
    "allow_move": True,
    "vary_length": True,
    "continue_dancing": True,
    "anim_speed": 1.0,
    "idle_frequency": 2,
    "mute_all": False,
    "music_on": True,
    "sfx_on": True,
    "music_volume": 0.45,
    "sfx_volume": 0.55,
    "current_track": "__RANDOM__",
    "playlist_autoplay": True,
    "scale": 2,
    "opacity": 1.0,
    "gravity_on": True,
    "lock_position": False,
    "pinned_x": None,
    "pinned_y": None,
    "ghost_mode": False,
    "hide_fullscreen": True,
    "force_over_fullscreen": False,
    "monitor_index": 0,
    "show_splash": True,
    "run_at_startup": False
}

CLASSIC_1998_PRESET = {
    "allow_move": True,
    "vary_length": True,
    "continue_dancing": True,
    "anim_speed": 1.0,
    "idle_frequency": 2,
    "mute_all": False,
    "music_on": True,
    "sfx_on": True,
    "music_volume": 0.50,
    "sfx_volume": 0.60,
    "playlist_autoplay": False,
    "scale": 1,
    "opacity": 1.0,
    "gravity_on": True,
    "lock_position": False,
    "ghost_mode": False,
    "hide_fullscreen": False,
    "force_over_fullscreen": False,
    "monitor_index": 0,
    "show_splash": True,
    "run_at_startup": False
}


class CharacterManager:
    JAPAN_ANIM_RANGES = {
        "Walk_R": [0, 23],
        "Walk_L": [24, 47],
        "Idle": [48, 71],
        "Run_R": [72, 91],
        "Run_L": [92, 111],
        "Spin": [112, 131],
        "Jump_R": [132, 155],
        "Jump_L": [156, 179],
        "Squash_R": [180, 190],
        "Squash_L": [191, 201]
    }

    def __init__(self):
        default_sprites = resolve_asset_dir("assets/sprites", "sprites")
        default_audio = resolve_asset_dir("assets/audio", "audio")
        self.characters = {
            "crash_jp_1998": {
                "id": "crash_jp_1998",
                "name": "Crash Bandicoot (Japan 1998)",
                "sprites_dir": default_sprites,
                "audio_dir": default_audio,
                "animations": dict(self.JAPAN_ANIM_RANGES)
            }
        }
        self.scan_external_characters(default_audio)

    def scan_external_characters(self, fallback_audio):
        app_dir = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))
        search_roots = [os.path.join(app_dir, "characters"), resource_path("characters")]
        seen = set()
        for root_dir in search_roots:
            if not os.path.isdir(root_dir):
                continue
            for folder in sorted(os.listdir(root_dir)):
                char_path = os.path.join(root_dir, folder)
                if not os.path.isdir(char_path) or folder in seen:
                    continue
                sprites_dir = os.path.join(char_path, "sprites")
                if not os.path.isdir(sprites_dir):
                    continue
                seen.add(folder)
                meta_file = os.path.join(char_path, "character.json")
                char_name = folder.replace("_", " ")
                anims = dict(self.JAPAN_ANIM_RANGES)
                if os.path.exists(meta_file):
                    try:
                        with open(meta_file, "r", encoding="utf-8") as f:
                            meta = json.load(f)
                            char_name = meta.get("name", char_name)
                            if isinstance(meta.get("animations"), dict):
                                anims.update(meta["animations"])
                    except Exception:
                        pass
                audio_dir = os.path.join(char_path, "audio")
                if not os.path.isdir(audio_dir):
                    audio_dir = fallback_audio
                self.characters[folder] = {
                    "id": folder,
                    "name": char_name,
                    "sprites_dir": sprites_dir,
                    "audio_dir": audio_dir,
                    "animations": anims
                }

    def get_character(self, char_id):
        return self.characters.get(char_id) or self.characters["crash_jp_1998"]


class LanguageManager:
    def __init__(self):
        self.languages = {"en": dict(FALLBACK_EN)}
        self.load_all_languages()

    def load_all_languages(self):
        lang_dir = resolve_asset_dir("assets/lang", "lang")
        if not os.path.isdir(lang_dir):
            return
        for fname in sorted(os.listdir(lang_dir)):
            if fname.lower().endswith(".json") and not fname.upper().startswith("TEMPLATE"):
                code = os.path.splitext(fname)[0]
                full_path = os.path.join(lang_dir, fname)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        loaded = json.load(f)
                        merged = dict(FALLBACK_EN)
                        merged.update(loaded)
                        self.languages[code] = merged
                except Exception:
                    pass

    def available_languages(self):
        items = []
        if "en" in self.languages:
            items.append(("en", self.languages["en"].get("_lang_name", "English")))
        for code, data in self.languages.items():
            if code != "en":
                items.append((code, data.get("_lang_name", code)))
        return items

    def tr(self, lang_code, key, **kwargs):
        lang_dict = self.languages.get(lang_code) or self.languages["en"]
        text = lang_dict.get(key, FALLBACK_EN.get(key, key))
        if kwargs:
            try:
                return text.format(**kwargs)
            except Exception:
                return text
        return text


class GlobalHotkeyFilter(QAbstractNativeEventFilter):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def nativeEventFilter(self, eventType, message):
        if IS_WINDOWS and eventType == b"windows_generic_MSG":
            msg = wintypes.MSG.from_address(int(message))
            if msg.message == 0x0312 and msg.wParam == HOTKEY_RESCUE_ID:
                self.callback()
                return True, 0
        return False, 0


class RetroToast(QLabel):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool | Qt.WindowTransparentForInput)
        self.setStyleSheet(
            "background-color: rgba(25, 25, 30, 225);"
            "color: #ff9f1a;"
            "border: 2px solid #ff9f1a;"
            "border-radius: 6px;"
            "padding: 6px 12px;"
            "font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;"
            "font-size: 12px;"
            "font-weight: bold;"
        )
        self.hide_timer = QTimer(self)
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.hide)

    def show_message(self, text, anchor_rect, duration_ms=2200):
        self.setText(text)
        self.adjustSize()
        x = anchor_rect.left() + (anchor_rect.width() - self.width()) // 2
        y = max(10, anchor_rect.top() - self.height() - 8)
        self.move(x, y)
        self.show()
        self.raise_()
        self.hide_timer.start(duration_ms)


def load_global_settings():
    data = dict(DEFAULT_SETTINGS)
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data.update(json.load(f))
        except Exception:
            pass
    return data


def set_system_wallpaper(filepath):
    abs_path = os.path.abspath(filepath)
    if IS_WINDOWS:
        ctypes.windll.user32.SystemParametersInfoW(0x0014, 0, abs_path, 0x03)
    elif IS_MACOS:
        script = f'tell application "Finder" to set desktop picture to POSIX file "{abs_path}"'
        subprocess.run(["osascript", "-e", script], check=True)
    elif IS_LINUX:
        uri = f"file://{abs_path}"
        subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", uri], check=False)
        subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri-dark", uri], check=False)


class AboutDialog(QDialog):
    def __init__(self, mascot, parent=None):
        super().__init__(parent)
        self.setWindowTitle(mascot.tr("win_about_title"))
        if mascot.primary_mascot.settings.get("language") == "ar":
            self.setLayoutDirection(Qt.RightToLeft)
        layout = QVBoxLayout(self)
        lbl = QLabel()
        pix = QPixmap(resource_path("assets/about.png"))
        if not pix.isNull():
            lbl.setPixmap(pix)
        else:
            lbl.setText(
                "Mascot Crash Bandicoot (1998 - Japan Edition)\n"
                "マスコット・クラッシュ・バンディクー\n"
                "Original Software by SME Intermedia Inc. / flagship inc.\n"
                "Cross-Platform Remaster by @Hitsuji_Shiroi (2026)"
            )
        btn = QPushButton("OK")
        btn.clicked.connect(self.accept)
        layout.addWidget(lbl)
        layout.addWidget(btn)


class OptionsDialog(QDialog):
    SPEED_VALUES = [0.5, 1.0, 1.5, 2.0]

    def __init__(self, mascot, parent=None, initial_tab=0):
        super().__init__(parent)
        self.mascot = mascot
        self.primary = mascot.primary_mascot
        self.settings = self.primary.settings
        self.setFixedSize(640, 610)

        self.extras_root = resolve_asset_dir("assets/extras", "extras")
        self.preview_player = QMediaPlayer(self)
        self.preview_audio = QAudioOutput(self)
        self.preview_audio.setVolume(0.75)
        self.preview_player.setAudioOutput(self.preview_audio)

        self.tabs = QTabWidget()
        self.tabs.addTab(self._build_classic_tab(), "")
        self.tabs.addTab(self._build_audio_tab(), "")
        self.tabs.addTab(self._build_desktop_tab(), "")
        self.tabs.addTab(self._build_extras_tab(), "")
        self.tabs.setCurrentIndex(initial_tab)

        bottom_row = QHBoxLayout()
        self.btn_reset = QPushButton()
        self.btn_reset.clicked.connect(self.reset_defaults)
        self.btn_ok = QPushButton()
        self.btn_ok.clicked.connect(self.save_and_close)
        bottom_row.addWidget(self.btn_reset)
        bottom_row.addStretch()
        bottom_row.addWidget(self.btn_ok)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.tabs)
        main_layout.addLayout(bottom_row)

        self.retranslate_ui()
        self.load_ui_from_dict(self.settings)

    def closeEvent(self, event):
        self.preview_player.stop()
        super().closeEvent(event)

    def tr_key(self, key, **kwargs):
        return self.primary.lang_mgr.tr(self.current_lang_code(), key, **kwargs)

    def current_lang_code(self):
        if hasattr(self, "combo_lang") and self.combo_lang.currentData():
            return self.combo_lang.currentData()
        return self.settings.get("language", "en")

    def _build_classic_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        self.grp_rules = QGroupBox()
        lay_rules = QVBoxLayout(self.grp_rules)
        self.cb_move = QCheckBox()
        self.cb_vary = QCheckBox()
        self.cb_continue = QCheckBox()
        for w in (self.cb_move, self.cb_vary, self.cb_continue):
            lay_rules.addWidget(w)

        self.grp_timing = QGroupBox()
        form = QFormLayout(self.grp_timing)

        self.combo_char = QComboBox()
        for cid, cdata in self.primary.char_mgr.characters.items():
            self.combo_char.addItem(cdata["name"], cid)
        idx_char = self.combo_char.findData(self.settings.get("character_id", "crash_jp_1998"))
        if idx_char != -1:
            self.combo_char.setCurrentIndex(idx_char)

        self.combo_lang = QComboBox()
        for code, name in self.primary.lang_mgr.available_languages():
            self.combo_lang.addItem(name, code)
        idx_lang = self.combo_lang.findData(self.settings.get("language", "en"))
        if idx_lang != -1:
            self.combo_lang.setCurrentIndex(idx_lang)
        self.combo_lang.currentIndexChanged.connect(self.on_language_changed)

        self.combo_speed = QComboBox()
        self.combo_idle = QComboBox()

        self.lbl_character = QLabel()
        self.lbl_language = QLabel()
        self.lbl_dance_speed = QLabel()
        self.lbl_spontaneous = QLabel()

        form.addRow(self.lbl_character, self.combo_char)
        form.addRow(self.lbl_language, self.combo_lang)
        form.addRow(self.lbl_dance_speed, self.combo_speed)
        form.addRow(self.lbl_spontaneous, self.combo_idle)

        layout.addWidget(self.grp_rules)
        layout.addWidget(self.grp_timing)
        layout.addStretch()
        return tab

    def _build_audio_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        self.btn_mute_all = QPushButton()
        self.btn_mute_all.setCheckable(True)
        self.btn_mute_all.toggled.connect(self.update_audio_controls_state)
        layout.addWidget(self.btn_mute_all)

        self.grp_music = QGroupBox()
        lay_music = QVBoxLayout(self.grp_music)

        row_m_vol = QHBoxLayout()
        self.cb_music = QCheckBox()
        self.slider_music_vol = QSlider(Qt.Horizontal)
        self.slider_music_vol.setRange(0, 100)
        self.slider_music_vol.valueChanged.connect(
            lambda v: self.primary.audio_output.setVolume(0.0 if self.btn_mute_all.isChecked() else v / 100.0)
        )
        row_m_vol.addWidget(self.cb_music)
        row_m_vol.addWidget(self.slider_music_vol)

        form_ost = QFormLayout()
        self.combo_track = QComboBox()
        self.combo_track.currentIndexChanged.connect(self.on_track_selected)
        self.lbl_selected_track = QLabel()
        form_ost.addRow(self.lbl_selected_track, self.combo_track)

        self.lbl_now_playing = QLabel()
        self.lbl_now_playing.setStyleSheet("font-weight: bold; color: #d35400;")

        row_transport = QHBoxLayout()
        self.btn_prev = QPushButton()
        self.btn_play_pause = QPushButton()
        self.btn_next = QPushButton()
        self.btn_prev.clicked.connect(lambda: self._step_track(-1))
        self.btn_play_pause.clicked.connect(self.on_play_pause_clicked)
        self.btn_next.clicked.connect(lambda: self._step_track(1))
        for b in (self.btn_prev, self.btn_play_pause, self.btn_next):
            row_transport.addWidget(b)

        self.cb_autoplay = QCheckBox()

        lay_music.addLayout(row_m_vol)
        lay_music.addLayout(form_ost)
        lay_music.addWidget(self.lbl_now_playing)
        lay_music.addLayout(row_transport)
        lay_music.addWidget(self.cb_autoplay)

        self.grp_sfx = QGroupBox()
        row_sfx = QHBoxLayout(self.grp_sfx)
        self.cb_sfx = QCheckBox()
        self.slider_sfx_vol = QSlider(Qt.Horizontal)
        self.slider_sfx_vol.setRange(0, 100)
        row_sfx.addWidget(self.cb_sfx)
        row_sfx.addWidget(self.slider_sfx_vol)

        layout.addWidget(self.grp_music)
        layout.addWidget(self.grp_sfx)
        layout.addStretch()
        return tab

    def _build_desktop_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        self.grp_display = QGroupBox()
        form_vis = QFormLayout(self.grp_display)
        self.combo_scale = QComboBox()
        self.slider_opacity = QSlider(Qt.Horizontal)
        self.slider_opacity.setRange(30, 100)
        self.combo_monitor = QComboBox()

        self.lbl_scale = QLabel()
        self.lbl_opacity = QLabel()
        self.lbl_screen = QLabel()
        form_vis.addRow(self.lbl_scale, self.combo_scale)
        form_vis.addRow(self.lbl_opacity, self.slider_opacity)
        form_vis.addRow(self.lbl_screen, self.combo_monitor)

        self.grp_fs = QGroupBox()
        lay_fs = QVBoxLayout(self.grp_fs)
        self.cb_hide_fs = QCheckBox()
        self.cb_force_fs = QCheckBox()
        self.cb_hide_fs.toggled.connect(lambda c: self.cb_force_fs.setChecked(False) if c else None)
        self.cb_force_fs.toggled.connect(lambda c: self.cb_hide_fs.setChecked(False) if c else None)
        lay_fs.addWidget(self.cb_hide_fs)
        lay_fs.addWidget(self.cb_force_fs)

        self.grp_sys = QGroupBox()
        lay_sys = QVBoxLayout(self.grp_sys)
        self.cb_gravity = QCheckBox()
        self.cb_lock_pos = QCheckBox()
        self.cb_splash = QCheckBox()
        self.cb_startup = QCheckBox()
        self.cb_ghost = QCheckBox()
        self.lbl_hotkey_info = QLabel()
        self.lbl_hotkey_info.setStyleSheet("color: #555555; font-size: 11px;")
        self.cb_gravity.toggled.connect(lambda c: self.cb_lock_pos.setChecked(False) if c else None)
        for w in (self.cb_gravity, self.cb_lock_pos, self.cb_splash, self.cb_startup, self.cb_ghost, self.lbl_hotkey_info):
            lay_sys.addWidget(w)

        layout.addWidget(self.grp_display)
        layout.addWidget(self.grp_fs)
        layout.addWidget(self.grp_sys)
        layout.addStretch()
        return tab

    def _build_extras_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        top_bar = QHBoxLayout()
        self.combo_ext_cat = QComboBox()
        self.combo_ext_cat.currentIndexChanged.connect(self.on_extras_category_changed)
        self.btn_ext_open_dir = QPushButton()
        self.btn_ext_open_dir.clicked.connect(self.on_open_extras_folder)
        top_bar.addWidget(self.combo_ext_cat, stretch=1)
        top_bar.addWidget(self.btn_ext_open_dir)
        layout.addLayout(top_bar)

        mid_split = QHBoxLayout()
        self.list_ext_items = QListWidget()
        self.list_ext_items.setFixedWidth(225)
        self.list_ext_items.currentItemChanged.connect(self.on_extras_item_selected)

        preview_box = QFrame()
        preview_box.setFrameShape(QFrame.StyledPanel)
        preview_box.setStyleSheet("background-color: #18181c; border-radius: 6px;")
        preview_lay = QVBoxLayout(preview_box)

        self.lbl_ext_preview = QLabel("Select an item to preview")
        self.lbl_ext_preview.setAlignment(Qt.AlignCenter)
        self.lbl_ext_preview.setStyleSheet("color: #dddddd; font-size: 12px;")
        self.lbl_ext_preview.setMinimumSize(340, 340)

        self.lbl_ext_info = QLabel("")
        self.lbl_ext_info.setAlignment(Qt.AlignCenter)
        self.lbl_ext_info.setStyleSheet("color: #ff9f1a; font-weight: bold; font-size: 11px;")

        preview_lay.addWidget(self.lbl_ext_preview, stretch=1)
        preview_lay.addWidget(self.lbl_ext_info)

        mid_split.addWidget(self.list_ext_items)
        mid_split.addWidget(preview_box, stretch=1)
        layout.addLayout(mid_split, stretch=1)

        action_bar = QHBoxLayout()
        self.btn_ext_wallpaper = QPushButton()
        self.btn_ext_wallpaper.clicked.connect(self.on_apply_wallpaper)

        self.btn_ext_play = QPushButton()
        self.btn_ext_play.clicked.connect(self.on_play_extra_media)

        self.btn_ext_export_icons = QPushButton()
        self.btn_ext_export_icons.clicked.connect(self.on_export_all_icons)

        self.btn_ext_save = QPushButton()
        self.btn_ext_save.clicked.connect(self.on_save_selected_extra)

        for b in (self.btn_ext_wallpaper, self.btn_ext_play, self.btn_ext_export_icons, self.btn_ext_save):
            action_bar.addWidget(b)
        layout.addLayout(action_bar)

        return tab

    def _scan_extras_files(self, cat_key):
        results = []
        if cat_key == "wallpapers":
            wp_base = os.path.join(self.extras_root, "wallpapers")
            preferred_dirs = ["1280x1024", "1152x864", "1024x768", "800x600", "640x480"]
            seen_names = set()
            for res_dir in preferred_dirs:
                full_sub = os.path.join(wp_base, res_dir)
                if not os.path.isdir(full_sub):
                    continue
                for fn in sorted(os.listdir(full_sub)):
                    if fn.lower().endswith((".bmp", ".jpg", ".png")) and fn not in seen_names:
                        seen_names.add(fn)
                        results.append((f"{os.path.splitext(fn)[0]} [{res_dir}]", os.path.join(full_sub, fn)))
            if not results and os.path.isdir(wp_base):
                for root, _, files in os.walk(wp_base):
                    for fn in sorted(files):
                        if fn.lower().endswith((".bmp", ".jpg", ".png")):
                            results.append((fn, os.path.join(root, fn)))

        elif cat_key == "icons":
            ico_dir = os.path.join(self.extras_root, "icons")
            if os.path.isdir(ico_dir):
                for fn in sorted(os.listdir(ico_dir)):
                    if fn.lower().endswith(".ico"):
                        results.append((fn, os.path.join(ico_dir, fn)))

        elif cat_key == "gallery":
            gal_dir = os.path.join(self.extras_root, "gallery")
            if os.path.isdir(gal_dir):
                for fn in sorted(os.listdir(gal_dir)):
                    if fn.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".lgo")):
                        results.append((fn, os.path.join(gal_dir, fn)))

        elif cat_key == "videos":
            vid_dir = os.path.join(self.extras_root, "videos")
            if os.path.isdir(vid_dir):
                for fn in sorted(os.listdir(vid_dir)):
                    if fn.lower().endswith((".avi", ".mp4", ".wmv")):
                        results.append((fn, os.path.join(vid_dir, fn)))

        elif cat_key == "sfx":
            sfx_dir = os.path.join(self.extras_root, "sfx")
            if os.path.isdir(sfx_dir):
                for fn in sorted(os.listdir(sfx_dir)):
                    if fn.lower().endswith((".wav", ".mp3")):
                        results.append((fn, os.path.join(sfx_dir, fn)))

        return results

    def on_extras_category_changed(self):
        self.preview_player.stop()
        cat_key = self.combo_ext_cat.currentData()
        self.list_ext_items.clear()
        self.lbl_ext_preview.clear()
        self.lbl_ext_info.setText("")

        items = self._scan_extras_files(cat_key)
        for label, fpath in items:
            item = QListWidgetItem(label)
            item.setData(Qt.UserRole, fpath)
            if cat_key == "icons":
                item.setIcon(QIcon(fpath))
            self.list_ext_items.addItem(item)

        self.btn_ext_wallpaper.setVisible(cat_key == "wallpapers")
        self.btn_ext_export_icons.setVisible(cat_key == "icons")
        self.btn_ext_play.setVisible(cat_key in ("videos", "sfx"))
        self.btn_ext_save.setVisible(cat_key in ("wallpapers", "gallery", "icons", "videos", "sfx"))

        if self.list_ext_items.count() > 0:
            self.list_ext_items.setCurrentRow(0)
        else:
            self.lbl_ext_preview.setText(f"No files found in:\n{os.path.join(self.extras_root, cat_key or '')}")

    def on_extras_item_selected(self, current, _previous):
        self.preview_player.stop()
        if not current:
            return
        fpath = current.data(Qt.UserRole)
        cat_key = self.combo_ext_cat.currentData()
        if not fpath or not os.path.exists(fpath):
            return

        size_kb = max(1, os.path.getsize(fpath) // 1024)
        if cat_key in ("wallpapers", "gallery"):
            pix = QPixmap(fpath)
            if not pix.isNull():
                scaled = pix.scaled(350, 330, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.lbl_ext_preview.setPixmap(scaled)
                self.lbl_ext_info.setText(f"{os.path.basename(fpath)}  |  {pix.width()}x{pix.height()} px  |  {size_kb} KB")
            else:
                self.lbl_ext_preview.setText(os.path.basename(fpath))
                self.lbl_ext_info.setText(f"{size_kb} KB")

        elif cat_key == "icons":
            ico = QIcon(fpath)
            pix = ico.pixmap(QSize(64, 64))
            if not pix.isNull():
                big_pix = pix.scaled(128, 128, Qt.KeepAspectRatio, Qt.FastTransformation)
                self.lbl_ext_preview.setPixmap(big_pix)
            self.lbl_ext_info.setText(f"{os.path.basename(fpath)}  |  1998 Icon (32x32)  |  {size_kb} KB")

        elif cat_key == "videos":
            self.lbl_ext_preview.setPixmap(QPixmap())
            self.lbl_ext_preview.setText(
                f"🎬 MACS Resident Animation (flagship Inc. 1998)\n\n"
                f"File: {os.path.basename(fpath)}\n"
                f"Click 'Play Media' below to watch"
            )
            self.lbl_ext_info.setText(f"{os.path.basename(fpath)}  |  AVI Video  |  {size_kb} KB")

        elif cat_key == "sfx":
            self.lbl_ext_preview.setPixmap(QPixmap())
            self.lbl_ext_preview.setText(
                f"🔊 1998 Screensaver Voice / Sound Effect\n\n"
                f"File: {os.path.basename(fpath)}\n"
                f"Click 'Play Media' below to listen"
            )
            self.lbl_ext_info.setText(f"{os.path.basename(fpath)}  |  WAV Audio  |  {size_kb} KB")

    def on_apply_wallpaper(self):
        current = self.list_ext_items.currentItem()
        if not current:
            return
        fpath = os.path.abspath(current.data(Qt.UserRole))
        if os.path.exists(fpath):
            try:
                set_system_wallpaper(fpath)
                QMessageBox.information(self, "Wallpaper", self.tr_key("ext_msg_wp_ok"))
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

    def on_play_extra_media(self):
        current = self.list_ext_items.currentItem()
        if not current:
            return
        fpath = os.path.abspath(current.data(Qt.UserRole))
        cat_key = self.combo_ext_cat.currentData()
        if cat_key == "sfx":
            self.preview_player.setSource(QUrl.fromLocalFile(fpath))
            self.preview_player.play()
        elif cat_key == "videos":
            QDesktopServices.openUrl(QUrl.fromLocalFile(fpath))

    def on_save_selected_extra(self):
        current = self.list_ext_items.currentItem()
        if not current:
            return
        fpath = current.data(Qt.UserRole)
        if not os.path.exists(fpath):
            return
        dest_path, _ = QFileDialog.getSaveFileName(self, "Save File", os.path.basename(fpath))
        if dest_path:
            shutil.copy2(fpath, dest_path)

    def on_export_all_icons(self):
        ico_dir = os.path.join(self.extras_root, "icons")
        if not os.path.isdir(ico_dir):
            return
        target_dir = QFileDialog.getExistingDirectory(self, "Select Destination Folder for Icons")
        if not target_dir:
            return
        out_sub = os.path.join(target_dir, "Crash_Bandicoot_Japan_1998_Icons")
        os.makedirs(out_sub, exist_ok=True)
        count = 0
        for fn in os.listdir(ico_dir):
            if fn.lower().endswith(".ico"):
                shutil.copy2(os.path.join(ico_dir, fn), os.path.join(out_sub, fn))
                count += 1
        QMessageBox.information(self, "Icons Exported", self.tr_key("ext_msg_icons_ok", count=count, path=out_sub))

    def on_open_extras_folder(self):
        cat_key = self.combo_ext_cat.currentData() or ""
        target = os.path.join(self.extras_root, cat_key)
        if not os.path.isdir(target):
            target = self.extras_root
        if os.path.isdir(target):
            QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.abspath(target)))

    def retranslate_ui(self):
        code = self.current_lang_code()
        self.setLayoutDirection(Qt.RightToLeft if code == "ar" else Qt.LeftToRight)
        self.setWindowTitle(self.tr_key("win_options_title"))

        self.tabs.setTabText(0, self.tr_key("tab_classic"))
        self.tabs.setTabText(1, self.tr_key("tab_audio"))
        self.tabs.setTabText(2, self.tr_key("tab_desktop"))
        self.tabs.setTabText(3, self.tr_key("tab_extras"))

        self.grp_rules.setTitle(self.tr_key("grp_1998"))
        self.cb_move.setText(self.tr_key("cb_allow_move"))
        self.cb_vary.setText(self.tr_key("cb_vary_length"))
        self.cb_continue.setText(self.tr_key("cb_continue_dancing"))

        self.grp_timing.setTitle(self.tr_key("grp_timing"))
        self.lbl_character.setText(self.tr_key("lbl_character"))
        self.lbl_language.setText(self.tr_key("lbl_language"))
        self.lbl_dance_speed.setText(self.tr_key("lbl_dance_speed"))
        self.lbl_spontaneous.setText(self.tr_key("lbl_spontaneous"))

        cur_spd_idx = max(0, self.combo_speed.currentIndex())
        self.combo_speed.blockSignals(True)
        self.combo_speed.clear()
        self.combo_speed.addItems([
            self.tr_key("spd_slow"),
            self.tr_key("spd_normal"),
            self.tr_key("spd_fast"),
            self.tr_key("spd_turbo")
        ])
        self.combo_speed.setCurrentIndex(cur_spd_idx)
        self.combo_speed.blockSignals(False)

        cur_idle_idx = max(0, self.combo_idle.currentIndex())
        self.combo_idle.blockSignals(True)
        self.combo_idle.clear()
        self.combo_idle.addItems([
            self.tr_key("idle_never"),
            self.tr_key("idle_rarely"),
            self.tr_key("idle_normal"),
            self.tr_key("idle_hyper")
        ])
        self.combo_idle.setCurrentIndex(cur_idle_idx)
        self.combo_idle.blockSignals(False)

        self.grp_music.setTitle(self.tr_key("grp_music"))
        self.cb_music.setText(self.tr_key("cb_enable_music"))
        self.lbl_selected_track.setText(self.tr_key("lbl_selected_track"))

        cur_trk_data = self.combo_track.currentData() or self.settings.get("current_track", "__RANDOM__")
        self.populate_tracks(cur_trk_data)

        self.btn_prev.setText(self.tr_key("btn_prev"))
        self.btn_next.setText(self.tr_key("btn_next"))
        self.cb_autoplay.setText(self.tr_key("cb_autoplay"))

        self.grp_sfx.setTitle(self.tr_key("grp_sfx"))
        self.cb_sfx.setText(self.tr_key("cb_enable_sfx"))

        self.grp_display.setTitle(self.tr_key("grp_display"))
        self.lbl_scale.setText(self.tr_key("lbl_scale"))
        self.lbl_opacity.setText(self.tr_key("lbl_opacity"))
        self.lbl_screen.setText(self.tr_key("lbl_screen"))

        cur_scale_idx = max(0, self.combo_scale.currentIndex())
        self.combo_scale.blockSignals(True)
        self.combo_scale.clear()
        self.combo_scale.addItems([
            self.tr_key("scale_1x"),
            self.tr_key("scale_2x"),
            self.tr_key("scale_3x"),
            self.tr_key("scale_4x")
        ])
        self.combo_scale.setCurrentIndex(cur_scale_idx)
        self.combo_scale.blockSignals(False)

        cur_mon_idx = max(0, self.combo_monitor.currentIndex())
        self.combo_monitor.blockSignals(True)
        self.combo_monitor.clear()
        for idx, scr in enumerate(QApplication.screens()):
            geo = scr.geometry()
            self.combo_monitor.addItem(self.tr_key("lbl_monitor_item", num=idx + 1, w=geo.width(), h=geo.height()))
        self.combo_monitor.setCurrentIndex(min(cur_mon_idx, self.combo_monitor.count() - 1))
        self.combo_monitor.blockSignals(False)

        self.grp_fs.setTitle(self.tr_key("grp_fs"))
        self.cb_hide_fs.setText(self.tr_key("cb_hide_fs"))
        self.cb_force_fs.setText(self.tr_key("cb_force_fs"))

        self.grp_sys.setTitle(self.tr_key("grp_sys"))
        self.cb_gravity.setText(self.tr_key("cb_gravity"))
        self.cb_lock_pos.setText(self.tr_key("cb_lock_pos"))
        self.cb_splash.setText(self.tr_key("cb_splash"))
        self.cb_startup.setText(self.tr_key("cb_startup"))
        self.cb_ghost.setText(self.tr_key("cb_ghost"))
        self.lbl_hotkey_info.setText(self.tr_key("lbl_hotkey_info"))

        cur_ext_cat = self.combo_ext_cat.currentData() or "wallpapers"
        self.combo_ext_cat.blockSignals(True)
        self.combo_ext_cat.clear()
        for ckey, trk in (
            ("wallpapers", "ext_cat_wallpapers"),
            ("icons", "ext_cat_icons"),
            ("gallery", "ext_cat_gallery"),
            ("videos", "ext_cat_videos"),
            ("sfx", "ext_cat_sfx")
        ):
            self.combo_ext_cat.addItem(self.tr_key(trk), ckey)
        idx_ext = self.combo_ext_cat.findData(cur_ext_cat)
        self.combo_ext_cat.setCurrentIndex(idx_ext if idx_ext != -1 else 0)
        self.combo_ext_cat.blockSignals(False)

        self.btn_ext_open_dir.setText(self.tr_key("ext_btn_open_folder"))
        self.btn_ext_wallpaper.setText(self.tr_key("ext_btn_wallpaper"))
        self.btn_ext_save.setText(self.tr_key("ext_btn_save"))
        self.btn_ext_export_icons.setText(self.tr_key("ext_btn_export_icons"))
        self.btn_ext_play.setText(self.tr_key("ext_btn_play"))
        self.on_extras_category_changed()

        self.btn_reset.setText(self.tr_key("btn_reset_1998"))
        self.btn_ok.setText(self.tr_key("btn_apply_ok"))

        self.update_audio_controls_state(self.btn_mute_all.isChecked())
        self.refresh_transport_ui()

    def on_language_changed(self):
        self.settings["language"] = self.current_lang_code()
        self.retranslate_ui()
        self.primary.rebuild_tray_menu()

    def load_ui_from_dict(self, cfg, first_track_on_reset=False):
        self.cb_move.setChecked(cfg["allow_move"])
        self.cb_vary.setChecked(cfg["vary_length"])
        self.cb_continue.setChecked(cfg["continue_dancing"])

        idx_spd = self.SPEED_VALUES.index(cfg["anim_speed"]) if cfg["anim_speed"] in self.SPEED_VALUES else 1
        self.combo_speed.setCurrentIndex(idx_spd)
        self.combo_idle.setCurrentIndex(cfg["idle_frequency"])

        self.btn_mute_all.setChecked(cfg["mute_all"])
        self.cb_music.setChecked(cfg["music_on"])
        self.slider_music_vol.setValue(int(cfg["music_volume"] * 100))

        self.populate_tracks(cfg.get("current_track", "__RANDOM__"))
        if first_track_on_reset and self.combo_track.count() > 1:
            self.combo_track.setCurrentIndex(1)

        self.cb_autoplay.setChecked(cfg["playlist_autoplay"])
        self.cb_sfx.setChecked(cfg["sfx_on"])
        self.slider_sfx_vol.setValue(int(cfg["sfx_volume"] * 100))

        self.combo_scale.setCurrentIndex(min(cfg["scale"] - 1, 3))
        self.slider_opacity.setValue(int(cfg["opacity"] * 100))
        self.combo_monitor.setCurrentIndex(min(cfg["monitor_index"], self.combo_monitor.count() - 1))
        self.cb_hide_fs.setChecked(cfg["hide_fullscreen"])
        self.cb_force_fs.setChecked(cfg["force_over_fullscreen"])
        self.cb_gravity.setChecked(cfg["gravity_on"])
        self.cb_lock_pos.setChecked(cfg["lock_position"])
        self.cb_splash.setChecked(cfg["show_splash"])
        self.cb_startup.setChecked(cfg["run_at_startup"])
        self.cb_ghost.setChecked(cfg["ghost_mode"])

        self.update_audio_controls_state(self.btn_mute_all.isChecked())
        self.refresh_transport_ui()

    def populate_tracks(self, preferred_track="__RANDOM__"):
        self.combo_track.blockSignals(True)
        self.combo_track.clear()
        self.combo_track.addItem(self.tr_key("opt_random_track"), "__RANDOM__")
        for name in self.primary.music_tracks.keys():
            self.combo_track.addItem(name, name)
        idx = self.combo_track.findData(preferred_track)
        self.combo_track.setCurrentIndex(idx if idx != -1 else 0)
        self.combo_track.blockSignals(False)

    def on_track_selected(self):
        track_val = self.combo_track.currentData()
        if track_val:
            self.settings["current_track"] = track_val
            self.primary.load_track_by_choice(track_val, auto_play=True)
            self.refresh_transport_ui()

    def _step_track(self, delta):
        self.primary.step_track(delta, show_toast=True)
        self.combo_track.blockSignals(True)
        idx = self.combo_track.findData(self.primary.current_playing_name)
        if idx != -1:
            self.combo_track.setCurrentIndex(idx)
        self.combo_track.blockSignals(False)
        self.refresh_transport_ui()

    def on_play_pause_clicked(self):
        if not self.cb_music.isChecked():
            self.cb_music.setChecked(True)
            self.settings["music_on"] = True
        self.primary.toggle_play_pause_music()
        self.refresh_transport_ui()

    def refresh_transport_ui(self):
        track_display = self.primary.current_playing_name or self.tr_key("txt_no_tracks")
        self.lbl_now_playing.setText(self.tr_key("lbl_now_playing", track=track_display))
        self.btn_play_pause.setText(self.tr_key("btn_pause") if self.primary.is_music_playing() else self.tr_key("btn_play"))

    def update_audio_controls_state(self, is_muted):
        self.btn_mute_all.setText(self.tr_key("btn_unmute_all") if is_muted else self.tr_key("btn_mute_all"))
        for w in (
            self.cb_music, self.slider_music_vol, self.combo_track,
            self.btn_prev, self.btn_play_pause, self.btn_next,
            self.cb_autoplay, self.cb_sfx, self.slider_sfx_vol
        ):
            w.setEnabled(not is_muted)

    def reset_defaults(self):
        self.load_ui_from_dict(CLASSIC_1998_PRESET, first_track_on_reset=True)

    def save_and_close(self):
        self.preview_player.stop()
        self.settings.update({
            "character_id": self.combo_char.currentData(),
            "language": self.current_lang_code(),
            "allow_move": self.cb_move.isChecked(),
            "vary_length": self.cb_vary.isChecked(),
            "continue_dancing": self.cb_continue.isChecked(),
            "anim_speed": self.SPEED_VALUES[self.combo_speed.currentIndex()],
            "idle_frequency": self.combo_idle.currentIndex(),
            "mute_all": self.btn_mute_all.isChecked(),
            "music_on": self.cb_music.isChecked(),
            "music_volume": self.slider_music_vol.value() / 100.0,
            "current_track": self.combo_track.currentData(),
            "playlist_autoplay": self.cb_autoplay.isChecked(),
            "sfx_on": self.cb_sfx.isChecked(),
            "sfx_volume": self.slider_sfx_vol.value() / 100.0,
            "scale": self.combo_scale.currentIndex() + 1,
            "opacity": self.slider_opacity.value() / 100.0,
            "monitor_index": self.combo_monitor.currentIndex(),
            "hide_fullscreen": self.cb_hide_fs.isChecked(),
            "force_over_fullscreen": self.cb_force_fs.isChecked(),
            "gravity_on": self.cb_gravity.isChecked(),
            "lock_position": self.cb_lock_pos.isChecked(),
            "show_splash": self.cb_splash.isChecked(),
            "run_at_startup": self.cb_startup.isChecked(),
            "ghost_mode": self.cb_ghost.isChecked()
        })
        self.accept()


class CrashMascotJapan1998(QLabel):
    ROAM_ACTIONS = [
        ("Walk", "move_walk"),
        ("Run", "move_run"),
        ("Spin", "move_spin"),
        ("Jump", "move_jump"),
        ("Squash", "move_squash")
    ]

    def __init__(self, settings, lang_mgr, char_mgr, is_clone=False, primary_mascot=None, spawn_offset=0):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.is_clone = is_clone
        self.primary_mascot = self if not is_clone else primary_mascot
        self.clones = [] if not is_clone else None

        self.settings = settings if not is_clone else dict(primary_mascot.settings)
        if is_clone:
            self.settings["lock_position"] = False
            self.settings["pinned_x"] = None
            self.settings["pinned_y"] = None

        self.lang_mgr = lang_mgr
        self.char_mgr = char_mgr
        self.toast = RetroToast() if not is_clone else primary_mascot.toast

        self.current_state = "Idle"
        self.is_full_dance_mode = False
        self.single_move_mode = False
        self.move_ticks_remaining = 0
        self.frame_index = 0
        self.direction = random.choice([-1, 1]) if is_clone else 1
        self.is_dragging = False
        self.velocity_y = 0
        self.jump_origin_y = 0
        self.drag_offset = QPoint()

        self.hidden_by_fullscreen = False
        self.music_was_playing_before_fs = False
        self.music_user_paused = False
        self.current_playing_name = ""

        if not is_clone:
            self.audio_output = QAudioOutput()
            self.music_player = QMediaPlayer()
            self.music_player.setAudioOutput(self.audio_output)
            self.music_player.mediaStatusChanged.connect(self.on_media_status_changed)
        else:
            self.audio_output = primary_mascot.audio_output
            self.music_player = primary_mascot.music_player

        self.sfx_players = []
        self.load_character_assets(self.settings.get("character_id", "crash_jp_1998"))

        self.apply_audio_settings()
        self.apply_window_settings(move_to_screen=True, spawn_offset=spawn_offset)

        if not is_clone:
            self.setup_tray_icon()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.update_timer_speed()

        self.fs_timer = QTimer(self)
        self.fs_timer.timeout.connect(self.check_fullscreen_state)
        self.fs_timer.start(500)

        if not is_clone and IS_WINDOWS:
            self.register_global_rescue_hotkey()

    def all_instances(self):
        p = self.primary_mascot
        return [p] + list(p.clones)

    def spawn_clone(self):
        p = self.primary_mascot
        offset = ((len(p.clones) + 1) * 55) * (1 if len(p.clones) % 2 == 0 else -1)
        clone = CrashMascotJapan1998(
            p.settings, p.lang_mgr, p.char_mgr,
            is_clone=True, primary_mascot=p, spawn_offset=offset
        )
        p.clones.append(clone)
        clone.show()
        if p.is_full_dance_mode:
            clone.start_dance()
        p.rebuild_tray_menu()
        p.toast.show_message(p.tr("toast_clone_spawned", count=len(p.all_instances())), clone.geometry())

    def remove_this_clone(self):
        if not self.is_clone:
            return
        p = self.primary_mascot
        self.timer.stop()
        self.fs_timer.stop()
        if self in p.clones:
            p.clones.remove(self)
        p.rebuild_tray_menu()
        self.close()
        self.deleteLater()

    def clear_all_clones(self):
        p = self.primary_mascot
        for c in list(p.clones):
            c.timer.stop()
            c.fs_timer.stop()
            c.close()
            c.deleteLater()
        p.clones.clear()
        p.rebuild_tray_menu()
        p.toast.show_message(p.tr("toast_clone_spawned", count=1), p.geometry())

    def dance_all_instances(self):
        for inst in self.all_instances():
            inst.start_dance()

    def stop_all_instances(self):
        for inst in self.all_instances():
            inst.stop_crash()

    def register_global_rescue_hotkey(self):
        if not IS_WINDOWS:
            return
        try:
            ctypes.windll.user32.RegisterHotKey(None, HOTKEY_RESCUE_ID, 0x0002 | 0x0004 | 0x4000, 0x43)
        except Exception:
            pass

    def rescue_character(self):
        p = self.primary_mascot
        for idx, inst in enumerate(p.all_instances()):
            inst.settings.update({
                "ghost_mode": False,
                "lock_position": False,
                "pinned_x": None,
                "pinned_y": None
            })
            inst.hidden_by_fullscreen = False
            offset = (idx * 50) * (1 if idx % 2 == 0 else -1)
            inst.apply_window_settings(move_to_screen=True, spawn_offset=offset)
            inst.raise_()
        p.save_settings()
        p.activateWindow()
        p.rebuild_tray_menu()
        p.toast.show_message(p.tr("toast_rescued"), p.geometry())

    def tr(self, key, **kwargs):
        return self.primary_mascot.lang_mgr.tr(self.primary_mascot.settings.get("language", "en"), key, **kwargs)

    def save_settings(self):
        if self.is_clone:
            return
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=2)
        except Exception:
            pass

    def configure_system_startup(self, enable):
        try:
            if IS_WINDOWS:
                startup_dir = os.path.join(
                    os.environ.get("APPDATA", ""),
                    r"Microsoft\Windows\Start Menu\Programs\Startup"
                )
                if not os.path.isdir(startup_dir):
                    return
                bat_path = os.path.join(startup_dir, "CrashBandicootDesktopJapan1998.bat")
                if enable:
                    if getattr(sys, 'frozen', False):
                        target = f'start "" "{sys.executable}"'
                    else:
                        script_path = os.path.abspath(__file__)
                        target = f'cd /d "{os.path.dirname(script_path)}"\nstart "" pyw "{script_path}"'
                    with open(bat_path, "w", encoding="utf-8") as f:
                        f.write(f"@echo off\n{target}\n")
                elif os.path.exists(bat_path):
                    os.remove(bat_path)

            elif IS_MACOS:
                agents_dir = os.path.expanduser("~/Library/LaunchAgents")
                os.makedirs(agents_dir, exist_ok=True)
                plist_path = os.path.join(agents_dir, "com.hitsujishiroi.crashmascotjapan1998.plist")
                if enable:
                    exec_cmd = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
                    plist_content = (
                        '<?xml version="1.0" encoding="UTF-8"?>\n'
                        '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n'
                        '<plist version="1.0"><dict>\n'
                        '  <key>Label</key><string>com.hitsujishiroi.crashmascotjapan1998</string>\n'
                        f'  <key>ProgramArguments</key><array><string>{exec_cmd}</string></array>\n'
                        '  <key>RunAtLoad</key><true/>\n'
                        '</dict></plist>\n'
                    )
                    with open(plist_path, "w", encoding="utf-8") as f:
                        f.write(plist_content)
                elif os.path.exists(plist_path):
                    os.remove(plist_path)

            elif IS_LINUX:
                autostart_dir = os.path.expanduser("~/.config/autostart")
                os.makedirs(autostart_dir, exist_ok=True)
                desktop_path = os.path.join(autostart_dir, "CrashBandicootDesktopJapan1998.desktop")
                if enable:
                    exec_cmd = f'"{sys.executable}"' if getattr(sys, 'frozen', False) else f'python3 "{os.path.abspath(__file__)}"'
                    with open(desktop_path, "w", encoding="utf-8") as f:
                        f.write(
                            "[Desktop Entry]\n"
                            "Type=Application\n"
                            "Name=Mascot Crash Bandicoot (Japan 1998)\n"
                            f"Exec={exec_cmd}\n"
                            "X-GNOME-Autostart-enabled=true\n"
                        )
                elif os.path.exists(desktop_path):
                    os.remove(desktop_path)
        except Exception:
            pass

    def is_fullscreen_active(self):
        if not IS_WINDOWS:
            return False
        try:
            state = ctypes.c_int()
            if ctypes.windll.shell32.SHQueryUserNotificationState(ctypes.byref(state)) == 0 and state.value in (2, 3, 4):
                return True

            hwnd = ctypes.windll.user32.GetForegroundWindow()
            if not hwnd or hwnd == int(self.winId()):
                return False

            class_buf = ctypes.create_unicode_buffer(256)
            ctypes.windll.user32.GetClassNameW(hwnd, class_buf, 256)
            if class_buf.value in ("Progman", "WorkerW", "Shell_TrayWnd", "Shell_SecondaryTrayWnd"):
                return False

            rect = wintypes.RECT()
            if ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect)):
                screens = QApplication.screens()
                mon_geo = screens[min(self.settings.get("monitor_index", 0), len(screens) - 1)].geometry()
                return (
                    rect.left <= mon_geo.left() + 2
                    and rect.top <= mon_geo.top() + 2
                    and rect.right >= mon_geo.right() - 1
                    and rect.bottom >= mon_geo.bottom() - 1
                )
        except Exception:
            pass
        return False

    def check_fullscreen_state(self):
        if self.settings.get("force_over_fullscreen", False):
            if self.hidden_by_fullscreen:
                self.hidden_by_fullscreen = False
                self.show()
            if IS_WINDOWS:
                try:
                    ctypes.windll.user32.SetWindowPos(int(self.winId()), -1, 0, 0, 0, 0, 0x0013)
                except Exception:
                    pass
            return

        if self.settings.get("hide_fullscreen", True):
            fs_now = self.is_fullscreen_active()
            if fs_now and not self.hidden_by_fullscreen:
                self.hidden_by_fullscreen = True
                if not self.is_clone:
                    self.music_was_playing_before_fs = self.is_music_playing()
                    if self.music_was_playing_before_fs:
                        self.music_player.pause()
                self.hide()
            elif not fs_now and self.hidden_by_fullscreen:
                self.hidden_by_fullscreen = False
                self.show()
                if not self.is_clone and self.music_was_playing_before_fs and self.settings["music_on"] and not self.settings.get("mute_all", False):
                    self.music_player.play()
        elif self.hidden_by_fullscreen:
            self.hidden_by_fullscreen = False
            self.show()

    def load_character_assets(self, char_id):
        self.active_char = self.char_mgr.get_character(char_id)
        self.settings["character_id"] = self.active_char["id"]
        self.reload_sprites()
        self.music_tracks, self.sfx_list = self.classify_audios(self.active_char["audio_dir"])

        for eff in self.sfx_players:
            eff.deleteLater()
        self.sfx_players = []
        for sfx_path in self.sfx_list:
            eff = QSoundEffect(self)
            eff.setSource(QUrl.fromLocalFile(sfx_path))
            self.sfx_players.append(eff)

        if not self.is_clone:
            was_playing = self.is_music_playing()
            self.load_track_by_choice(self.settings.get("current_track", "__RANDOM__"), auto_play=was_playing)
        self.apply_audio_settings()

    def set_character(self, char_id):
        for inst in self.all_instances():
            inst.load_character_assets(char_id)
            inst.apply_window_settings(move_to_screen=False)
        self.primary_mascot.save_settings()
        self.primary_mascot.rebuild_tray_menu()

    def get_wav_duration(self, filepath):
        try:
            with wave.open(filepath, 'rb') as w:
                rate = w.getframerate()
                return w.getnframes() / float(rate) if rate > 0 else 0
        except Exception:
            return 5.0 if os.path.getsize(filepath) > 45 * 1024 else 1.0

    def classify_audios(self, audio_dir):
        tracks = {}
        sfx = []
        if not os.path.isdir(audio_dir):
            return tracks, sfx

        seen_sizes = set()
        for root, _, files in os.walk(audio_dir):
            rel_folder = os.path.relpath(root, audio_dir).lower()
            for fname in sorted(files):
                lower_f = fname.lower()
                if not lower_f.endswith((".mp3", ".wav", ".ogg")):
                    continue
                full_path = os.path.join(root, fname)
                clean_name = os.path.splitext(fname)[0]
                file_size = os.path.getsize(full_path)

                if "sfx" in rel_folder:
                    sfx.append(full_path)
                    continue

                if lower_f.endswith(".wav"):
                    duration = self.get_wav_duration(full_path)
                    if file_size in seen_sizes and clean_name.lower().startswith("bgmdata"):
                        continue
                    seen_sizes.add(file_size)
                    clean_name = f"{clean_name} ({max(1, int(duration))}s)"

                tracks[clean_name] = full_path

        return tracks, sfx

    def is_music_playing(self):
        return self.primary_mascot.music_player.playbackState() == QMediaPlayer.PlayingState

    def load_track_by_choice(self, choice, auto_play=True, show_toast=False):
        p = self.primary_mascot
        tracks_dict = p.music_tracks
        if not tracks_dict:
            p.current_playing_name = ""
            return
        names = list(tracks_dict.keys())
        chosen_name = random.choice(names) if (choice == "__RANDOM__" or choice not in tracks_dict) else choice
        path = tracks_dict[chosen_name]
        if os.path.exists(path):
            p.current_playing_name = chosen_name
            p.music_player.setSource(QUrl.fromLocalFile(path))
            if auto_play and not p.hidden_by_fullscreen and p.settings["music_on"] and not p.settings.get("mute_all", False):
                p.music_user_paused = False
                p.music_player.play()
            if show_toast and not p.hidden_by_fullscreen:
                p.toast.show_message(p.tr("toast_now_playing", track=chosen_name), self.geometry())

    def step_track(self, delta, from_end=False, show_toast=False):
        p = self.primary_mascot
        tracks_dict = p.music_tracks
        if not tracks_dict:
            return
        names = list(tracks_dict.keys())
        cur_idx = names.index(p.current_playing_name) if p.current_playing_name in names else 0
        target_name = names[(cur_idx + delta) % len(names)]
        if not from_end:
            p.settings["current_track"] = target_name
            p.save_settings()
        should_play = True if from_end else (p.is_music_playing() or not p.music_user_paused)
        self.load_track_by_choice(target_name, auto_play=should_play, show_toast=show_toast)

    def on_media_status_changed(self, status):
        if status != QMediaPlayer.EndOfMedia or not self.settings["music_on"] or self.settings.get("mute_all", False) or self.music_user_paused:
            return
        if self.settings.get("current_track") == "__RANDOM__":
            self.load_track_by_choice("__RANDOM__", auto_play=True)
        elif self.settings.get("playlist_autoplay", True):
            self.step_track(1, from_end=True)
        else:
            self.music_player.setPosition(0)
            self.music_player.play()

    def toggle_play_pause_music(self):
        p = self.primary_mascot
        if p.is_music_playing():
            p.music_user_paused = True
            p.music_player.pause()
        else:
            if not p.music_player.source().isValid():
                p.load_track_by_choice(p.settings.get("current_track", "__RANDOM__"), auto_play=False)
            if p.music_player.source().isValid():
                p.settings["music_on"] = True
                p.settings["mute_all"] = False
                p.music_user_paused = False
                p.apply_audio_settings()
                p.music_player.play()
                p.save_settings()

    def set_quick_volume(self, level):
        p = self.primary_mascot
        p.settings["music_volume"] = level
        p.settings["mute_all"] = False
        p.save_settings()
        p.apply_audio_settings()

    def apply_audio_settings(self):
        p = self.primary_mascot
        is_muted = p.settings.get("mute_all", False)
        if not self.is_clone:
            self.audio_output.setVolume(0.0 if is_muted else p.settings.get("music_volume", 0.45))
            if is_muted or not p.settings["music_on"] or p.hidden_by_fullscreen:
                self.music_player.pause()
        sfx_vol = 0.0 if is_muted else p.settings.get("sfx_volume", 0.55)
        for eff in self.sfx_players:
            eff.setVolume(sfx_vol)

    def play_random_sfx(self):
        p = self.primary_mascot
        if not self.hidden_by_fullscreen and not p.settings.get("mute_all", False) and p.settings["sfx_on"] and self.sfx_players:
            random.choice(self.sfx_players).play()

    def apply_window_settings(self, move_to_screen=False, spawn_offset=0):
        self.setWindowOpacity(self.settings.get("opacity", 1.0))
        self.setAttribute(Qt.WA_TransparentForMouseEvents, self.settings.get("ghost_mode", False))

        screens = QApplication.screens()
        self.screen_rect = screens[min(self.settings.get("monitor_index", 0), len(screens) - 1)].availableGeometry()
        self.update_sprite()

        if self.settings.get("lock_position", False) and self.settings.get("pinned_x") is not None:
            self.move(self.settings["pinned_x"], self.settings["pinned_y"])
        elif move_to_screen or not self.screen_rect.contains(self.geometry().center()):
            base_x = self.screen_rect.left() + (self.screen_rect.width() - self.width()) // 2 + spawn_offset
            clamped_x = max(self.screen_rect.left(), min(base_x, self.screen_rect.right() - self.width()))
            self.move(clamped_x, self.screen_rect.bottom() - self.height() - 5)
        if not self.hidden_by_fullscreen:
            self.show()

    def update_timer_speed(self):
        self.timer.start(max(20, int(55 / self.settings.get("anim_speed", 1.0))))

    def reload_sprites(self):
        anim_ranges = self.active_char["animations"]
        sprites_dir = self.active_char["sprites_dir"]
        self.animations = {}
        for state_name, (start_idx, end_idx) in anim_ranges.items():
            self.animations[state_name] = self.load_range(sprites_dir, start_idx, end_idx)

    def load_range(self, sprites_dir, start_idx, end_idx):
        frames = []
        s = self.settings["scale"]
        for i in range(start_idx, end_idx + 1):
            pix = QPixmap(os.path.join(sprites_dir, f"frame_{i:03d}.png"))
            if not pix.isNull():
                frames.append(pix.scaled(pix.width() * s, pix.height() * s, Qt.KeepAspectRatio, Qt.FastTransformation))
        return frames

    def _resolve_directional_key(self):
        suffix = "_R" if self.direction == 1 else "_L"
        directional_key = f"{self.current_state}{suffix}"
        if directional_key in self.animations and self.animations[directional_key]:
            return directional_key, False
        if self.current_state in self.animations and self.animations[self.current_state]:
            return self.current_state, (self.direction == -1 and self.current_state not in ("Idle", "Spin"))
        return "Idle", False

    def update_sprite(self):
        anim_key, need_mirror = self._resolve_directional_key()
        frames = self.animations.get(anim_key) or self.animations.get("Idle", [])
        if not frames:
            return
        pix = frames[self.frame_index % len(frames)]
        if need_mirror:
            pix = pix.transformed(QTransform().scale(-1, 1))
        self.setPixmap(pix)
        self.resize(pix.size())

    def get_active_window_top(self):
        if not IS_WINDOWS:
            return self.screen_rect.bottom()
        try:
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            if hwnd and hwnd != int(self.winId()):
                rect = wintypes.RECT()
                if ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect)):
                    center_x = self.x() + self.width() // 2
                    if rect.left <= center_x <= rect.right and rect.top > self.screen_rect.top() + 40:
                        return rect.top
        except Exception:
            pass
        return self.screen_rect.bottom()

    def _move_horizontally(self, speed_px):
        if not self.settings.get("allow_move", True) or self.settings.get("lock_position", False):
            return
        new_x = self.x() + (speed_px * self.direction)
        if new_x <= self.screen_rect.left():
            new_x = self.screen_rect.left()
            self.direction = 1
        elif new_x + self.width() >= self.screen_rect.right():
            new_x = self.screen_rect.right() - self.width()
            self.direction = -1
        self.move(new_x, self.y())

    def tick(self):
        if self.is_dragging or self.hidden_by_fullscreen:
            return

        locked = self.settings.get("lock_position", False)
        if locked:
            px, py = self.settings.get("pinned_x"), self.settings.get("pinned_y")
            if px is not None and py is not None and (self.x() != px or self.y() != py):
                self.move(px, py)

        self.frame_index += 1
        scale = self.settings.get("scale", 2)

        if not locked:
            if self.settings.get("gravity_on", True):
                floor_y = self.screen_rect.bottom() - self.height()
                win_top = self.get_active_window_top() - self.height()
                target_y = win_top if (self.y() <= win_top + 14 and win_top < floor_y) else floor_y
            else:
                target_y = self.jump_origin_y if self.current_state == "Jump" else self.y()

            if self.y() < target_y or self.velocity_y < 0:
                self.velocity_y += 3
                new_y = min(self.y() + self.velocity_y, target_y)
                self.move(self.x(), new_y)
                if self.current_state == "Jump":
                    self._move_horizontally(5 * scale)
                if new_y >= target_y:
                    self.velocity_y = 0
                    if self.current_state == "Jump":
                        self.current_state = "Squash"
                        self.frame_index = 0
                        self.move_ticks_remaining = 11
                self.update_sprite()
                return
            self.velocity_y = 0

        if self.current_state == "Walk":
            self._move_horizontally(3 * scale)
        elif self.current_state == "Run":
            self._move_horizontally(7 * scale)
        elif self.current_state == "Spin":
            self._move_horizontally(4 * scale)

        if self.current_state != "Idle":
            self.move_ticks_remaining -= 1
            if self.move_ticks_remaining <= 0:
                if self.is_full_dance_mode:
                    self.pick_next_dance_move()
                elif self.single_move_mode:
                    self.single_move_mode = False
                    if self.settings["continue_dancing"]:
                        self.start_dance()
                    else:
                        self.stop_crash()
                else:
                    self.current_state = "Idle"
        else:
            prob = [0.0, 0.005, 0.02, 0.07][min(self.settings.get("idle_frequency", 2), 3)]
            if random.random() < prob:
                move_state = random.choice([m[0] for m in self.ROAM_ACTIONS])
                self.trigger_single_move(move_state, from_idle=True)

        self.update_sprite()

    def get_move_duration(self, state_name):
        if state_name == "Squash":
            return 11
        if state_name == "Jump":
            return 24
        return random.randint(24, 52) if self.settings["vary_length"] else 36

    def _apply_action_physics(self, state_name):
        if state_name == "Jump" and not self.settings.get("lock_position", False):
            self.jump_origin_y = self.y()
            self.velocity_y = -24

    def pick_next_dance_move(self):
        self.current_state = random.choice([m[0] for m in self.ROAM_ACTIONS])
        self.frame_index = 0
        self.move_ticks_remaining = self.get_move_duration(self.current_state)
        if random.random() < 0.45:
            self.direction = random.choice([-1, 1])
        self._apply_action_physics(self.current_state)
        self.play_random_sfx()

    def start_dance(self):
        p = self.primary_mascot
        self.is_full_dance_mode = True
        self.single_move_mode = False
        self.pick_next_dance_move()
        if not self.is_clone:
            if not p.music_player.source().isValid():
                p.load_track_by_choice(p.settings.get("current_track", "__RANDOM__"), auto_play=False)
            if (
                not p.hidden_by_fullscreen
                and not p.settings.get("mute_all", False)
                and p.settings["music_on"]
                and not p.music_user_paused
                and p.music_player.source().isValid()
            ):
                p.music_player.play()

    def stop_crash(self):
        self.is_full_dance_mode = False
        self.single_move_mode = False
        self.current_state = "Idle"
        self.frame_index = 0
        self.velocity_y = 0
        if not self.is_clone:
            self.music_player.stop()
        self.update_sprite()

    def trigger_single_move(self, move_name, from_idle=False):
        self.is_full_dance_mode = False
        self.single_move_mode = not from_idle
        self.current_state = move_name
        self.frame_index = 0
        self.move_ticks_remaining = self.get_move_duration(move_name)
        self._apply_action_physics(move_name)
        self.play_random_sfx()
        self.update_sprite()

    def toggle_quick_setting(self, key):
        p = self.primary_mascot
        if key in ("lock_position", "gravity_on", "ghost_mode"):
            self.settings[key] = not self.settings[key]
            if key == "lock_position":
                self.settings["pinned_x"] = self.x() if self.settings["lock_position"] else None
                self.settings["pinned_y"] = self.y() if self.settings["lock_position"] else None
            elif key == "gravity_on" and self.settings["gravity_on"]:
                self.settings.update({"lock_position": False, "pinned_x": None, "pinned_y": None})
            if not self.is_clone:
                p.save_settings()
            self.apply_window_settings(move_to_screen=False)
        else:
            p.settings[key] = not p.settings[key]
            if key == "hide_fullscreen" and p.settings["hide_fullscreen"]:
                p.settings["force_over_fullscreen"] = False
            elif key == "force_over_fullscreen" and p.settings["force_over_fullscreen"]:
                p.settings["hide_fullscreen"] = False
            p.save_settings()
            for inst in p.all_instances():
                inst.settings[key] = p.settings[key]
                inst.settings["hide_fullscreen"] = p.settings["hide_fullscreen"]
                inst.settings["force_over_fullscreen"] = p.settings["force_over_fullscreen"]
                inst.check_fullscreen_state()
                inst.apply_audio_settings()

        p.rebuild_tray_menu()

    def open_options(self, initial_tab=0):
        p = self.primary_mascot
        old_char = p.settings.get("character_id", "crash_jp_1998")
        old_scale = p.settings["scale"]
        old_mon = p.settings.get("monitor_index", 0)
        old_startup = p.settings.get("run_at_startup", False)

        if OptionsDialog(self, self, initial_tab=initial_tab).exec():
            locked = p.settings.get("lock_position", False)
            p.settings["pinned_x"] = p.x() if locked else None
            p.settings["pinned_y"] = p.y() if locked else None
            p.save_settings()

            if p.settings.get("run_at_startup", False) != old_startup:
                p.configure_system_startup(p.settings["run_at_startup"])

            for inst in p.all_instances():
                if inst.is_clone:
                    keep_x, keep_y = inst.x(), inst.y()
                    inst.settings.update(p.settings)
                    inst.settings["lock_position"] = False
                    inst.settings["pinned_x"] = None
                    inst.settings["pinned_y"] = None

                if p.settings.get("character_id") != old_char:
                    inst.load_character_assets(p.settings["character_id"])
                elif p.settings["scale"] != old_scale:
                    inst.reload_sprites()

                inst.update_timer_speed()
                inst.check_fullscreen_state()
                inst.apply_audio_settings()
                inst.apply_window_settings(move_to_screen=(p.settings.get("monitor_index", 0) != old_mon))
                if inst.is_clone and p.settings.get("monitor_index", 0) == old_mon:
                    inst.move(keep_x, keep_y)

            p.rebuild_tray_menu()

    def _make_check_action(self, text_key, setting_key, parent_menu, enabled=True, use_primary=False):
        target_cfg = self.primary_mascot.settings if use_primary else self.settings
        act = QAction(self.tr(text_key), self, checkable=True)
        act.setChecked(target_cfg.get(setting_key, False))
        act.setEnabled(enabled)
        act.triggered.connect(lambda: self.toggle_quick_setting(setting_key))
        parent_menu.addAction(act)
        return act

    def _populate_clones_menu(self, menu):
        p = self.primary_mascot
        total = len(p.all_instances())
        clone_menu = menu.addMenu(f"{self.tr('menu_clones')} ({total})")
        clone_menu.addAction(self.tr("act_spawn_clone"), self.spawn_clone)
        clone_menu.addSeparator()
        clone_menu.addAction(self.tr("act_dance_all"), self.dance_all_instances)
        clone_menu.addAction(self.tr("act_stop_all"), self.stop_all_instances)
        if total > 1:
            clone_menu.addSeparator()
            clone_menu.addAction(self.tr("act_clear_clones"), self.clear_all_clones)

    def _populate_character_menu(self, menu):
        if len(self.char_mgr.characters) <= 1:
            return
        char_menu = menu.addMenu(self.tr("menu_character"))
        grp = QActionGroup(self)
        grp.setExclusive(True)
        cur_cid = self.primary_mascot.settings.get("character_id", "crash_jp_1998")
        for cid, cdata in self.char_mgr.characters.items():
            act = QAction(cdata["name"], self, checkable=True)
            act.setChecked(cid == cur_cid)
            act.triggered.connect(lambda checked=False, c=cid: self.set_character(c))
            grp.addAction(act)
            char_menu.addAction(act)

    def _populate_position_menu(self, menu):
        self._make_check_action("act_hide_fs", "hide_fullscreen", menu, use_primary=True)
        self._make_check_action("act_force_fs", "force_over_fullscreen", menu, use_primary=True)
        menu.addSeparator()
        self._make_check_action("act_gravity", "gravity_on", menu)
        self._make_check_action("act_lock_pos", "lock_position", menu)

    def _populate_audio_menu(self, menu):
        p = self.primary_mascot
        is_muted = p.settings.get("mute_all", False)
        now_title = p.current_playing_name or self.tr("txt_no_tracks")
        act_now = QAction(f"♪ {now_title}", self)
        act_now.setEnabled(False)
        menu.addAction(act_now)

        for key, slot in (
            ("act_pause_music" if self.is_music_playing() else "act_play_music", self.toggle_play_pause_music),
            ("act_next_track", lambda: self.step_track(1, show_toast=True)),
            ("act_prev_track", lambda: self.step_track(-1, show_toast=True))
        ):
            act = QAction(self.tr(key), self)
            act.setEnabled(not is_muted)
            act.triggered.connect(slot)
            menu.addAction(act)

        menu.addSeparator()

        qvol_menu = menu.addMenu(self.tr("menu_quick_vol"))
        qvol_menu.setEnabled(not is_muted)
        vol_group = QActionGroup(self)
        vol_group.setExclusive(True)
        cur_vol = round(p.settings.get("music_volume", 0.45), 2)
        for pct, val in (("25%", 0.25), ("50%", 0.50), ("75%", 0.75), ("100%", 1.00)):
            act_v = QAction(pct, self, checkable=True)
            act_v.setChecked(abs(cur_vol - val) < 0.06)
            act_v.triggered.connect(lambda checked=False, v=val: self.set_quick_volume(v))
            vol_group.addAction(act_v)
            qvol_menu.addAction(act_v)

        self._make_check_action("act_mute_all", "mute_all", menu, use_primary=True)
        menu.addSeparator()
        self._make_check_action("act_enable_music", "music_on", menu, enabled=not is_muted, use_primary=True)
        self._make_check_action("act_sfx", "sfx_on", menu, enabled=not is_muted, use_primary=True)

    def rebuild_tray_menu(self):
        if self.is_clone:
            return
        tray_menu = QMenu()
        tray_menu.addAction(self.tr("menu_start_dance"), self.dance_all_instances)
        tray_menu.addAction(self.tr("menu_stop"), self.stop_all_instances)
        tray_menu.addAction(self.tr("menu_bring_center"), self.rescue_character)
        tray_menu.addSeparator()
        self._populate_clones_menu(tray_menu)
        self._populate_character_menu(tray_menu)
        self._populate_position_menu(tray_menu.addMenu(self.tr("menu_pos_fs")))
        self._populate_audio_menu(tray_menu.addMenu(self.tr("menu_vol_ost")))
        self._make_check_action("act_ghost_mode", "ghost_mode", tray_menu)
        tray_menu.addSeparator()
        tray_menu.addAction(self.tr("menu_extras"), lambda: self.open_options(initial_tab=3))
        tray_menu.addAction(f"{self.tr('menu_options')}...", lambda: self.open_options(initial_tab=0))
        tray_menu.addAction(self.tr("menu_exit"), QApplication.quit)
        self.tray.setContextMenu(tray_menu)

    def setup_tray_icon(self):
        self.tray = QSystemTrayIcon(self)
        sprites_dir = self.active_char["sprites_dir"]
        icon_pix = QPixmap(os.path.join(sprites_dir, "frame_048.png"))
        if icon_pix.isNull():
            icon_pix = QPixmap(os.path.join(sprites_dir, "frame_000.png"))
        if not icon_pix.isNull():
            self.tray.setIcon(QIcon(icon_pix))
        self.tray.setToolTip("Mascot Crash Bandicoot (Japan 1998)")
        self.rebuild_tray_menu()
        self.tray.activated.connect(lambda r: self.rescue_character() if r == QSystemTrayIcon.DoubleClick else None)
        self.tray.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self.settings.get("lock_position", False):
            self.is_dragging = True
            self.velocity_y = 0
            self.drag_offset = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
        elif event.button() == Qt.RightButton:
            self.show_menu(event.globalPosition().toPoint())

    def mouseMoveEvent(self, event):
        if self.is_dragging and not self.settings.get("lock_position", False) and (event.buttons() & Qt.LeftButton):
            self.move(event.globalPosition().toPoint() - self.drag_offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = False

    def show_menu(self, pos):
        menu = QMenu(self)
        if self.primary_mascot.settings.get("language") == "ar":
            menu.setLayoutDirection(Qt.RightToLeft)

        menu.addAction(self.tr("menu_start_dance"), self.start_dance)
        menu.addAction(self.tr("menu_stop"), self.stop_crash)
        menu.addSeparator()

        self._populate_clones_menu(menu)
        self._populate_character_menu(menu)

        anim_menu = menu.addMenu(self.tr("menu_animations"))
        anim_menu.addAction(
            self.tr("menu_random_move"),
            lambda: self.trigger_single_move(random.choice([m[0] for m in self.ROAM_ACTIONS]))
        )
        anim_menu.addSeparator()
        for move_state, move_key in self.ROAM_ACTIONS:
            anim_menu.addAction(self.tr(move_key), lambda checked=False, m=move_state: self.trigger_single_move(m))

        menu.addSeparator()
        self._populate_position_menu(menu.addMenu(self.tr("menu_pos_fs")))
        self._populate_audio_menu(menu.addMenu(self.tr("menu_vol_ost")))
        menu.addAction(self.tr("menu_extras"), lambda: self.open_options(initial_tab=3))
        menu.addAction(self.tr("menu_options"), lambda: self.open_options(initial_tab=0))
        menu.addAction(self.tr("menu_about"), lambda: AboutDialog(self, self).exec())
        menu.addSeparator()
        if self.is_clone:
            menu.addAction(self.tr("act_close_this"), self.remove_this_clone)
        menu.addAction(self.tr("menu_exit"), QApplication.quit)
        menu.exec(pos)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    probe_socket = QLocalSocket()
    probe_socket.connectToServer(SERVER_NAME)
    if probe_socket.waitForConnected(250):
        probe_socket.write(b"RESCUE")
        probe_socket.flush()
        probe_socket.waitForBytesWritten(250)
        probe_socket.disconnectFromServer()
        sys.exit(0)

    QLocalServer.removeServer(SERVER_NAME)
    instance_server = QLocalServer()
    instance_server.listen(SERVER_NAME)

    saved_settings = load_global_settings()
    lang_manager = LanguageManager()
    char_manager = CharacterManager()

    splash_path = resource_path("assets/splash.png")
    use_splash = saved_settings.get("show_splash", True) and os.path.exists(splash_path)

    splash = QSplashScreen(QPixmap(splash_path)) if use_splash else None
    if splash:
        splash.show()

    crash = CrashMascotJapan1998(saved_settings, lang_manager, char_manager)

    if IS_WINDOWS:
        hotkey_filter = GlobalHotkeyFilter(crash.rescue_character)
        app.installNativeEventFilter(hotkey_filter)
        app.aboutToQuit.connect(lambda: ctypes.windll.user32.UnregisterHotKey(None, HOTKEY_RESCUE_ID))

    def handle_secondary_instance():
        conn = instance_server.nextPendingConnection()
        if conn:
            conn.close()
        crash.rescue_character()

    instance_server.newConnection.connect(handle_secondary_instance)

    QTimer.singleShot(2000 if splash else 0, lambda: (splash.finish(crash) if splash else None, crash.show()))
    sys.exit(app.exec())
