def computed_reactive(**computed_props):
    """
    Creates reactive controls with computed properties.

    Usage:
    ```python
    @computed_reactive(
        text=lambda self: f"Count: {self.rx_count.value}",
        color=lambda self: "red" if self.rx_count.value > 10 else "blue"
    )
    class MyText(ft.Text):
        def __init__(self):
            self.rx_count = RxInt(0)
            super().__init__()
    ```
    """
    def decorator(cls):
        original_init = cls.__init__

        def __init__(self, *args, **kwargs):
            # Call the original constructor
            original_init(self, *args, **kwargs)

            # Helper to recompute all computed properties
            def _recompute():
                for name, func in computed_props.items():
                    setattr(self, name, func(self))

            # Compute initial values
            _recompute()

            # Attach listeners to all RxInt attributes
            for attr_name, attr_value in vars(self).items():
                if hasattr(attr_value, "add_listener"):
                    # Use a closure to capture the recompute function
                    attr_value.add_listener(lambda _: _recompute())

            # Store the recompute method for potential future use
            self._recompute_computed = _recompute

        cls.__init__ = __init__
        return cls

    return decorator