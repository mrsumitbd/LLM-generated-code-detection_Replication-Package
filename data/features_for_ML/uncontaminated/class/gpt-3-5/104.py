from typing import Type
import flet as ft

class FletXWidgetRegistry:
    """FletX Widget Registry
    This class manages the registration of FletX widgets with Flet.
    It allows widgets to be registered and ensures they are available
    for use in Flet applications.
    """

    registered_widgets = []

    @classmethod
    def register(cls, widget_class: Type[ft.Control]):
        cls.registered_widgets.append(widget_class)

    @classmethod
    def register_all(cls, page: ft.Page):
        for widget_class in cls.registered_widgets:
            page.add_widget(widget_class())