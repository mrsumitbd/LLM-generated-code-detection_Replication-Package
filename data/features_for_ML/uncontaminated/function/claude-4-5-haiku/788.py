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
        
        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            
            # Store computed property functions
            self._computed_props = computed_props
            self._computed_values = {}
            
            # Initialize computed properties
            for prop_name, compute_fn in computed_props.items():
                self._update_computed_prop(prop_name, compute_fn)
        
        def _update_computed_prop(self, prop_name, compute_fn):
            try:
                value = compute_fn(self)
                self._computed_values[prop_name] = value
                setattr(self, prop_name, value)
            except Exception:
                pass
        
        def _refresh_computed_props(self):
            for prop_name, compute_fn in self._computed_props.items():
                self._update_computed_prop(prop_name, compute_fn)
        
        cls.__init__ = new_init
        cls._update_computed_prop = _update_computed_prop
        cls._refresh_computed_props = _refresh_computed_props
        
        # Wrap property setters to trigger recomputation
        original_setattr = cls.__setattr__
        
        def new_setattr(self, name, value):
            original_setattr(self, name, value)
            if hasattr(self, '_computed_props'):
                self._refresh_computed_props()
        
        cls.__setattr__ = new_setattr
        
        return cls
    
    return decorator