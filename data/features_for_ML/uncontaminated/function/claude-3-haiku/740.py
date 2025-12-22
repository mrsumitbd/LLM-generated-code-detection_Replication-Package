def _add_model_arg_to_prop_calculators(self) -> None:
    """Add model argument to property calculators that only accept state.

    Transforms single-argument (state) property calculators to accept the
    dual-argument (state, model) interface by creating partial functions with an
    optional second argument.
    """
    for prop, calc in self.property_calculators.items():
        if calc.__code__.co_argcount == 1:
            self.property_calculators[prop] = partial(calc, model=self)