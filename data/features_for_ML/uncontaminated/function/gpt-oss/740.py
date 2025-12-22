import inspect
from functools import partial

def _add_model_arg_to_prop_calculators(self) -> None:
    """
    Add model argument to property calculators that only accept state.

    Transforms single-argument (state) property calculators to accept the
    dual-argument (state, model) interface by creating partial functions with an
    optional second argument.
    """
    # Iterate over a copy of items to avoid modifying the dict while iterating
    for prop_name, calc in list(self._prop_calculators.items()):
        # Skip if the calculator already accepts a model argument
        try:
            sig = inspect.signature(calc)
        except (ValueError, TypeError):
            # If we cannot inspect the signature, leave it unchanged
            continue

        # Count positional or keyword-only parameters
        pos_params = [
            p for p in sig.parameters.values()
            if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
        ]

        # If the calculator expects exactly one positional argument, wrap it
        if len(pos_params) == 1:
            # Define a wrapper that accepts an optional model argument
            def _wrapper(state, model=None, _calc=calc):
                return _calc(state)

            # Replace the original calculator with the wrapped version
            self._prop_calculators[prop_name] = _wrapper