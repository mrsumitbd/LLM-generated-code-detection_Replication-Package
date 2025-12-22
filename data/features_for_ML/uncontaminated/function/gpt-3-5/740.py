from functools import partial

def _add_model_arg_to_prop_calculators(self) -> None:
    for prop_name, prop_calc in self.property_calculators.items():
        if prop_calc.__code__.co_argcount == 1:
            self.property_calculators[prop_name] = partial(prop_calc, self.model)