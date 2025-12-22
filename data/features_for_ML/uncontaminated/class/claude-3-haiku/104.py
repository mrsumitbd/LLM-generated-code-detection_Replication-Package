from typing import Type
import flet as ft

class FletXWidgetRegistry:
    """FletX Widget Registry
    This class manages the registration of FletX widgets with Flet.
    It allows widgets to be registered and ensures they are available
    for use in Flet applications.
    """

    _registered_widgets = {}

    @classmethod
    def register(cls, widget_class: Type[ft.Control]):
        """Register a FletX widget with the registry.

        Args:
            widget_class (Type[ft.Control]): The widget class to be registered.
        """
        widget_name = widget_class.__name__
        if widget_name not in cls._registered_widgets:
            cls._registered_widgets[widget_name] = widget_class

    @classmethod
    def register_all(cls, page: ft.Page):
        """Register all registered FletX widgets with the given Flet page.

        Args:
            page (ft.Page): The Flet page to register the widgets with.
        """
        for widget_name, widget_class in cls._registered_widgets.items():
            page.register_control(widget_name, widget_class)