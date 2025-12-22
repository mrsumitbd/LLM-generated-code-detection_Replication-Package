from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, QHBoxLayout,
    QLineEdit, QLabel, QTableWidget, QTableWidgetItem, QComboBox, QFrame, QGroupBox, QHeaderView,
    QInputDialog, QMainWindow, QColorDialog, QAbstractItemView, QAbstractItemDelegate
)
from PyQt6.QtCore import Qt, QSettings

def choose_language():
    settings = QSettings("Vena", "Steam Achievement Localizer")
    current_language = settings.value("language", None)

    if current_language:
        return current_language  # Already saved language

    # Load available locales dynamically
    locales = load_available_locales()
    
    if not locales:
        return "English"  # Fallback if no locales found
    
    # Create language options from loaded locales
    lang_options = {}
    for locale_name, locale_info in locales.items():
        lang_options[locale_name] = locale_info['native_name']
    
    # Sort language options by priority
    sorted_names = get_sorted_locale_names(locales)
    sorted_options = [(name, lang_options[name]) for name in sorted_names if name in lang_options]
    
    lang, ok = QInputDialog.getItem(
        None,
        "Select Language",
        "Choose your language:",
        [display_name for name, display_name in sorted_options],
        0,
        False
    )
    
    if ok and lang:
        # Find the key for selected display name
        selected_key = None
        for name, display_name in sorted_options:
            if display_name == lang:
                selected_key = name
                break
        
        if selected_key:
            settings.setValue("language", selected_key)
            settings.sync()
            return selected_key

    # Default to first available locale or English
    default_locale = sorted_names[0] if sorted_names else "English"
    return default_locale