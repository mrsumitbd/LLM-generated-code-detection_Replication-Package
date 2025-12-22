class FletXWidgetRegistry:
    """FletX Widget Registry
    This class manages the registration of FletX widgets with Flet.
    It allows widgets to be registered and ensures they are available
    for use in Flet applications.
    """
    
    _registered_widgets: Dict[str, Type[ft.Control]] = {}

    @classmethod
    def register(cls, widget_class: Type[ft.Control]):
        """Register a single widget class"""
        widget_name = widget_class.__name__
        cls._registered_widgets[widget_name] = widget_class
        return widget_class

    @classmethod
    def register_all(cls, page: ft.Page):
        """Register all widgets with a Flet page"""
        for widget_name, widget_class in cls._registered_widgets.items():
            if not hasattr(page, widget_name):
                setattr(page, widget_name, widget_class)