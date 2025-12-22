def _add_model_arg_to_prop_calculators(self) -> None:
    """Add model argument to property calculators that only accept state.

    Transforms single-argument (state) property calculators to accept the
    dual-argument (state, model) interface by creating partial functions with an
    optional second argument.
    """
    import functools
    import inspect
    
    for prop_name, calculator in self.property_calculators.items():
        if callable(calculator):
            sig = inspect.signature(calculator)
            params = list(sig.parameters.values())
            
            # Check if calculator only accepts one parameter (state)
            if len(params) == 1:
                # Create a wrapper that accepts both state and model but ignores model
                def make_wrapper(calc):
                    @functools.wraps(calc)
                    def wrapper(state, model=None):
                        return calc(state)
                    return wrapper
                
                self.property_calculators[prop_name] = make_wrapper(calculator)