import os
import json
import platform
from PyQt5.QtGui import QColor, QFont, QFontDatabase
from PyQt5.QtWidgets import QApplication, QWidget, QStyleFactory

class ThemeManager:
    """Plugin for managing themes and fonts"""

    def __init__(self, main_window):
        self.main_window = main_window
        self._load_available_themes()
        self.current_theme = None
        self.current_font_weight = 'normal'
        self.current_font_size = 12
        self.current_accent_color_mode = 'system'
        self.custom_accent_color = None

    def _load_available_themes(self):
        self.available_themes = {}
        themes_dir = os.path.join(os.path.dirname(__file__), 'themes')
        for filename in os.listdir(themes_dir):
            if filename.endswith('.json'):
                with open(os.path.join(themes_dir, filename), 'r') as f:
                    theme_data = json.load(f)
                    theme_name = os.path.splitext(filename)[0]
                    self.available_themes[theme_name] = theme_data

    def get_available_theme_names(self):
        return list(self.available_themes.keys())

    def get_theme_display_name(self, theme_name, language_code='en'):
        if theme_name in self.available_themes:
            return self.available_themes[theme_name].get('display_name', theme_name)
        return theme_name

    def apply_palette_from_config(self, app, palette_config):
        palette = app.palette()
        for role, color in palette_config.items():
            palette.setColor(getattr(QPalette, role), QColor(color))
        app.setPalette(palette)

    def _apply_dark_palette(self, app):
        palette = app.palette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.white)
        app.setPalette(palette)

    def get_system_accent_color(self):
        if platform.system() == 'Windows':
            import winreg
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Accent')
                value, _ = winreg.QueryValueEx(key, 'AccentColor')
                winreg.CloseKey(key)
                return QColor((value & 0xFF0000) >> 16, (value & 0xFF00) >> 8, value & 0xFF)
            except:
                return QColor(92, 107, 192)  # Default Windows accent color
        elif platform.system() == 'Darwin':
            return QColor(0, 122, 255)  # Default macOS accent color
        else:
            return QColor(52, 101, 164)  # Default Linux accent color

    def get_theme_default_accent_color(self, theme_name=None):
        if theme_name is None:
            theme_name = self.current_theme
        if theme_name in self.available_themes:
            return QColor(self.available_themes[theme_name]['accent_color'])
        return self.get_system_accent_color()

    def is_system_dark(self):
        if platform.system() == 'Windows':
            import winreg
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Themes\Personalize')
                value, _ = winreg.QueryValueEx(key, 'AppsUseLightTheme')
                winreg.CloseKey(key)
                return value == 0
            except:
                return False
        elif platform.system() == 'Darwin':
            import CoreFoundation
            return CoreFoundation.CFPreferencesCopyAppValue('AppleInterfaceStyle', 'NSGlobalDomain') == 'Dark'
        else:
            return False

    def apply_styles_from_config(self, styles_config):
        self._clear_all_styles()
        for widget_type, style in styles_config.items():
            self._apply_style_to_widgets(widget_type, style)

    def _clear_all_styles(self):
        for widget in QApplication.allWidgets():
            widget.setStyleSheet('')

    def _apply_style_to_widgets(self, widget_type, style):
        for widget in self.main_window.findChildren(getattr(QWidget, widget_type)):
            widget.setStyleSheet(style)

    def set_theme(self, theme_name):
        if theme_name in self.available_themes:
            self.current_theme = theme_name
            self.apply_palette_from_config(QApplication.instance(), self.available_themes[theme_name]['palette'])
            self.apply_styles_from_config(self.available_themes[theme_name]['styles'])
            self.apply_font_to_widgets()

    def get_current_theme(self):
        return self.current_theme

    def apply_font_to_widgets(self):
        font = QFont(self.available_themes[self.current_theme]['font']['family'], self.current_font_size)
        font.setWeight(getattr(QFont, self.current_font_weight.upper()))
        QApplication.setFont(font)

    def set_font_weight(self, weight):
        self.current_font_weight = weight
        self.apply_font_to_widgets()

    def set_font_size(self, size):
        self.current_font_size = size
        self.apply_font_to_widgets()

    def get_current_font_weight(self):
        return self.current_font_weight

    def get_current_font_size(self):
        return self.current_font_size

    def set_accent_color(self, color_mode, custom_color=None):
        self.current_accent_color_mode = color_mode
        self.custom_accent_color = custom_color
        if color_mode == 'system':
            accent_color = self.get_system_accent_color()
        elif color_mode == 'theme_default':
            accent_color = self.get_theme_default_accent_color()
        else:
            accent_color = QColor(custom_color)
        self.apply_custom_accent_color(QApplication.instance(), accent_color)

    def get_current_accent_color_mode(self):
        return self.current_accent_color_mode

    def get_custom_accent_color(self):
        return self.custom_accent_color

    def apply_custom_accent_color(self, app, custom_color):
        palette = app.palette()
        palette.setColor(QPalette.Highlight, custom_color)
        palette.setColor(QPalette.HighlightedText, Qt.white)
        app.setPalette(palette)