import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class ThemeManager:
    """Plugin for managing themes and fonts"""

    def __init__(self, main_window):
        """
        Initialize the ThemeManager with a reference to the main window.
        """
        self.main_window = main_window
        self._themes = {}
        self._styles = {}
        self._current_theme = None
        self._font_weight = QtGui.QFont.Normal
        self._font_size = 10
        self._accent_color_mode = "system"  # or "custom"
        self._custom_accent_color = None

        self._load_available_themes()

    # ----------------------------------------------------------------------
    # Theme handling
    # ----------------------------------------------------------------------
    def _load_available_themes(self):
        """
        Load available themes. For simplicity we hard‑code a few themes.
        Each theme contains a display name per language and a default accent.
        """
        self._themes = {
            "light": {
                "display_name": {"en": "Light", "es": "Claro"},
                "accent": QtGui.QColor("#0066CC"),
                "palette": "light",
            },
            "dark": {
                "display_name": {"en": "Dark", "es": "Oscuro"},
                "accent": QtGui.QColor("#FF8800"),
                "palette": "dark",
            },
            "blue": {
                "display_name": {"en": "Blue", "es": "Azul"},
                "accent": QtGui.QColor("#0055FF"),
                "palette": "light",
            },
        }

    def get_available_theme_names(self):
        """Return a list of available theme identifiers."""
        return list(self._themes.keys())

    def get_theme_display_name(self, theme_name, language_code='en'):
        """Return the localized display name for a theme."""
        theme = self._themes.get(theme_name)
        if not theme:
            return theme_name
        return theme["display_name"].get(language_code, theme_name)

    def set_theme(self, theme_name):
        """Apply the specified theme."""
        if theme_name not in self._themes:
            raise ValueError(f"Unknown theme: {theme_name}")
        self._current_theme = theme_name
        theme = self._themes[theme_name]
        # Apply palette
        if theme["palette"] == "dark":
            self._apply_dark_palette(self.main_window)
        else:
            self.apply_palette_from_config(self.main_window, {})
        # Apply styles
        self.apply_styles_from_config(self._styles)
        # Apply font
        self.apply_font_to_widgets()
        # Apply accent
        if self._accent_color_mode == "custom" and self._custom_accent_color:
            self.apply_custom_accent_color(self.main_window, self._custom_accent_color)

    def get_current_theme(self):
        """Return the current theme name."""
        return self._current_theme

    # ----------------------------------------------------------------------
    # Palette handling
    # ----------------------------------------------------------------------
    def apply_palette_from_config(self, app, palette_config):
        """
        Apply a palette based on a configuration dictionary.
        The config may contain keys like 'window', 'text', 'highlight', etc.
        """
        palette = QtGui.QPalette()
        for role, color in palette_config.items():
            if isinstance(color, QtGui.QColor):
                palette.setColor(getattr(QtGui.QPalette, role), color)
            else:
                palette.setColor(getattr(QtGui.QPalette, role), QtGui.QColor(color))
        app.setPalette(palette)

    def _apply_dark_palette(self, app):
        """Set a simple dark palette."""
        dark = QtGui.QPalette()
        dark.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
        dark.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
        dark.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
        dark.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
        dark.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
        dark.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
        dark.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
        dark.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
        dark.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
        dark.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
        dark.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
        dark.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
        dark.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
        app.setPalette(dark)

    def get_system_accent_color(self):
        """Return the system accent color (highlight)."""
        return self.main_window.palette().color(QtGui.QPalette.Highlight)

    def get_theme_default_accent_color(self, theme_name=None):
        """Return the default accent color for a theme."""
        if theme_name is None:
            theme_name = self._current_theme
        theme = self._themes.get(theme_name)
        if theme:
            return theme["accent"]
        return self.get_system_accent_color()

    def is_system_dark(self):
        """Return True if the system palette is dark."""
        window_color = self.main_window.palette().color(QtGui.QPalette.Window)
        return window_color.lightness() < 128

    # ----------------------------------------------------------------------
    # Style handling
    # ----------------------------------------------------------------------
    def apply_styles_from_config(self, styles_config):
        """
        Apply styles to widgets. styles_config is a dict mapping widget
        class names to style sheet strings.
        """
        self._styles = styles_config
        self._clear_all_styles()
        for widget_type, style in styles_config.items():
            self._apply_style_to_widgets(widget_type, style)

    def _clear_all_styles(self):
        """Clear style sheets from all child widgets."""
        for widget in self.main_window.findChildren(QtWidgets.QWidget):
            widget.setStyleSheet("")

    def _apply_style_to_widgets(self, widget_type, style):
        """Apply a style sheet to all widgets of a given type."""
        for widget in self.main_window.findChildren(widget_type):
            widget.setStyleSheet(style)

    # ----------------------------------------------------------------------
    # Font handling
    # ----------------------------------------------------------------------
    def apply_font_to_widgets(self):
        """Apply the current font settings to all widgets."""
        font = QtGui.QFont()
        font.setWeight(self._font_weight)
        font.setPointSize(self._font_size)
        for widget in self.main_window.findChildren(QtWidgets.QWidget):
            widget.setFont(font)

    def set_font_weight(self, weight):
        """Set the font weight and apply."""
        self._font_weight = weight
        self.apply_font_to_widgets()

    def set_font_size(self, size):
        """Set the font size and apply."""
        self._font_size = size
        self.apply_font_to_widgets()

    def get_current_font_weight(self):
        """Return the current font weight."""
        return self._font_weight

    def get_current_font_size(self):
        """Return the current font size."""
        return self._font_size

    # ----------------------------------------------------------------------
    # Accent color handling
    # ----------------------------------------------------------------------
    def set_accent_color(self, color_mode, custom_color=None):
        """
        Set the accent color mode. color_mode can be 'system' or 'custom'.
        If 'custom', custom_color must be a QColor or hex string.
        """
        if color_mode not in ("system", "custom"):
            raise ValueError("color_mode must be 'system' or 'custom'")
        self._accent_color_mode = color_mode
        if color_mode == "custom":
            if isinstance(custom_color, QtGui.QColor):
                self._custom_accent_color = custom_color
            else:
                self._custom_accent_color = QtGui.QColor(custom_color)
            self.apply_custom_accent_color(self.main_window, self._custom_accent_color)
        else:
            self._custom_accent_color = None
            # Reapply system accent
            self.apply_palette_from_config(self.main_window, {})

    def get_current_accent_color_mode(self):
        """Return the current accent color mode."""
        return self._accent_color_mode

    def get_custom_accent_color(self):
        """Return the custom accent color if set."""
        return self._custom_accent_color

    def apply_custom_accent_color(self, app, custom_color):
        """Apply a custom accent color to the palette."""
        palette = app.palette()
        palette.setColor(QtGui.QPalette.Highlight, custom_color)
        palette.setColor(QtGui.QPalette.Button, custom_color.lighter(120))
        app.setPalette(palette)