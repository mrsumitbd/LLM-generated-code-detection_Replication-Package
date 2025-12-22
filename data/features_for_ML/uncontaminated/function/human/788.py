from fletx.core import (
    BindingType, BindingConfig, ComputedBindingConfig,
    FormFieldValidationRule
)

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
    computed_bindings = {}
    for prop, compute_fn in computed_props.items():
        computed_bindings[prop] = ComputedBindingConfig(
            compute_fn=lambda self=None, fn=compute_fn: fn(self),
            dependencies=['rx_count']  # You'd need to auto-detect this
        )
    
    return reactive_control(computed_bindings=computed_bindings)