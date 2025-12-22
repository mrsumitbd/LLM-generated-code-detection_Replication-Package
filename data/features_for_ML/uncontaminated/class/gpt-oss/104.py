from typing import Type, Dict
import flet as ft


class FletXWidgetRegistry:
    """FletX Widget Registry
    This class manages the registration of FletX widgets with Flet.
    It allows widgets to be registered and ensures they are available
    for use in Flet applications.
    """

    _registry: Dict[str, Type[ft.Control]] = {}

    @classmethod
    def register(cls, widget_class: Type[ft.Control]) -> None:
        """
        Register a single widget class.

        The widget name defaults to the class name but can be overridden
        by setting a ``__fletx_name__`` attribute on the class.
        """
        name = getattr(widget_class, "__fletx_name__", widget_class.__name__)
        cls._registry[name] = widget_class

    @classmethod
    def register_all(cls, page: ft.Page) -> None:
        """
        Register all stored widget classes with the given Flet page.
        """
        for name, widget_class in cls._registry.items():
            page.register_control(name, widget_class)