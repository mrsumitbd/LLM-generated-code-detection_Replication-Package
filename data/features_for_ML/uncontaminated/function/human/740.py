from functools import partial
import inspect

def _add_model_arg_to_prop_calculators(self) -> None:
        """Add model argument to property calculators that only accept state.

        Transforms single-argument (state) property calculators to accept the
        dual-argument (state, model) interface by creating partial functions with an
        optional second argument.
        """
        for frequency in self.prop_calculators:
            for name, prop_fn in self.prop_calculators[frequency].items():
                # Get function signature
                sig = inspect.signature(prop_fn)
                # If function only takes one parameter, wrap it to accept two
                if len(sig.parameters) == 1:
                    # we partially evaluate the function to create a new function with
                    # an optional second argument, this can be set to state later on
                    new_fn = partial(
                        lambda state, _=None, fn=None: (
                            None if fn is None else fn(state)
                        ),
                        fn=prop_fn,
                    )
                    self.prop_calculators[frequency][name] = new_fn