from typing import Callable, Any

class Implementation:
    def __init__(self, func: Callable, sig: Any, type_hints: dict, param_types: tuple):
        self.func = func
        self.sig = sig
        self.type_hints = type_hints
        self.param_types = param_types

    def __call__(self, *args, **kwargs):
        if len(args) != len(self.param_types):
            raise TypeError(f"Expected {len(self.param_types)} arguments, got {len(args)}")

        for i, arg in enumerate(args):
            if not isinstance(arg, self.param_types[i]):
                raise TypeError(f"Argument {i+1} must be of type {self.param_types[i]}")

        for key, value in kwargs.items():
            if key not in self.type_hints:
                raise TypeError(f"Unexpected keyword argument: {key}")
            if not isinstance(value, self.type_hints[key]):
                raise TypeError(f"Argument {key} must be of type {self.type_hints[key]}")

        return self.func(*args, **kwargs)