from typing import Callable, Any

class Implementation:

    def __init__(self, func: Callable, sig: Any, type_hints: dict, param_types: tuple):
        self.func = func
        self.sig = sig
        self.type_hints = type_hints
        self.param_types = param_types

# Example usage:
# impl = Implementation(my_func, "signature", {"param1": int, "param2": str}, (int, str))