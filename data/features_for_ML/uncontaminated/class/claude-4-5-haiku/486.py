class ThemeManager:
    """Plugin for managing themes and fonts"""

    def __init__(self, main_window):
        self.main_window = main_window
        self.current_theme = 'light'
        self.current_font_weight = 'normal'
        self.current_font_size = 10
        self.accent_color_mode = 'system'
        self.custom_accent_color = None
        self.available_themes = {}
        self.theme_translations = {}
        self._load_available_themes()

    def _load_available_themes(self):
        self.available_themes = {
            'light': {'name': 'Light', 'dark': False},
            'dark': {'name': 'Dark', 'dark': True},
            'auto': {'name': 'Auto', 'dark': None}
        }
        self.theme_translations = {
            'light': {'en': 'Light', 'es': 'Claro', 'fr': 'Clair'},
            'dark': {'en': 'Dark', 'es': 'Oscuro', 'fr': 'Sombre'},
            'auto': {'en': 'Auto', 'es': 'Automático', 'fr': 'Automatique'}
        }

    def get_available_theme_names(self):
        return list(self.available_themes.keys())

    def get_theme_display_name(self, theme_name, language_code='en'):
        if theme_name in self.theme_translations:
            return self.theme_translations[theme_name].get(language_code, 
                                                           self.available_themes[theme_name]['name'])
        return theme_name

    def apply_palette_from_config(self, app, palette_config):
        if isinstance(palette_config, dict):
            if palette_config.get('type') == 'dark':
                self._apply_dark_palette(app)
            elif palette_config.get('type') == 'light':
                self._apply_light_palette(app)
            elif palette_config.get('colors'):
                self._apply_custom_palette(app, palette_config['colors'])

    def _apply_dark_palette(self, app):
        from PyQt5.QtGui import QPalette, QColor
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        app.setPalette(palette)

    def _apply_light_palette(self, app):
        from PyQt5.QtGui import QPalette, QColor
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
        palette.setColor(QPalette.ToolTipBase, QColor(0, 0, 0))
        palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.Text, QColor(0, 0, 0))
        palette.setColor(QPalette.Button, QColor(240, 240, 240))
        palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Link, QColor(0, 0, 255))
        palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        app.setPalette(palette)

    def _apply_custom_palette(self, app, colors):
        from PyQt5.QtGui import QPalette, QColor
        palette = QPalette()
        for role, color in colors.items():
            try:
                palette_role = getattr(QPalette, role)
                palette.setColor(palette_role, QColor(color))
            except (AttributeError, ValueError):
                pass
        app.setPalette(palette)

    def get_system_accent_color(self):
        try:
            from PyQt5.QtGui import QColor
            return QColor(42, 130, 218)
        except:
            return None

    def get_theme_default_accent_color(self, theme_name=None):
        from PyQt5.QtGui import QColor
        if theme_name is None:
            theme_name = self.current_theme
        
        if theme_name == 'dark':
            return QColor(42, 130, 218)
        else:
            return QColor(0, 120, 215)

    def is_system_dark(self):
        try:
            from PyQt5.QtWidgets import QApplication
            palette = QApplication.instance().palette()
            return palette.color(palette.Window).lightness() < 128
        except:
            return False

    def apply_styles_from_config(self, styles_config):
        if isinstance(styles_config, dict):
            for widget_type, style in styles_config.items():
                self._apply_style_to_widgets(widget_type, style)

    def _clear_all_styles(self):
        if self.main_window:
            self.main_window.setStyleSheet("")

    def _apply_style_to_widgets(self, widget_type, style):
        if self.main_window:
            stylesheet = f"{widget_type} {{ {style} }}"
            current_sheet = self.main_window.styleSheet()
            self.main_window.setStyleSheet(current_sheet + "\n" + stylesheet)

    def set_theme(self, theme_name):
        if theme_name in self.available_themes:
            self.current_theme = theme_name
            return True
        return False

    def get_current_theme(self):
        return self.current_theme

    def apply_font_to_widgets(self):
        from PyQt5.QtGui import QFont
        if self.main_window:
            font = QFont()
            font.setPointSize(self.current_font_size)
            font.setWeight(QFont.Bold if self.current_font_weight == 'bold' else QFont.Normal)
            self.main_window.setFont(font)

    def set_font_weight(self, weight):
        if weight in ['normal', 'bold']:
            self.current_font_weight = weight
            self.apply_font_to_widgets()
            return True
        return False

    def set_font_size(self, size):
        if isinstance(size, int) and 6 <= size <= 32:
            self.current_font_size = size
            self.apply_font_to_widgets()
            return True
        return False

    def get_current_font_weight(self):
        return self.current_font_weight

    def get_current_font_size(self):
        return self.current_font_size

    def set_accent_color(self, color_mode, custom_color=None):
        if color_mode in ['system', 'custom']:
            self.accent_color_mode = color_mode
            if color_mode == 'custom' and custom_color:
                self.custom_accent_color = custom_color
            return True
        return False

    def get_current_accent_color_mode(self):
        return self.accent_color_mode

    def get_custom_accent_color(self):
        return self.custom_accent_color

    def apply_custom_accent_color(self, app, custom_color):
        from PyQt5.QtGui import QPalette, QColor
        if isinstance(custom_color, str):
            custom_color = QColor(custom_color)
        
        palette = app.palette()
        palette.setColor(QPalette.Highlight, custom_color)
        palette.setColor(QPalette.Link, custom_color)
        app.setPalette(palette)
        self.custom_accent_color = custom_color