from typing import (TypeVar, Callable, get_type_hints, overload as typing_overload,
                    Any, Type, Union, get_args, get_origin, cast)

class Implementation:
    __slots__ = ('func', 'sig', 'type_hints', 'param_types')
    func: Callable
    sig: Any  # Signature object
    type_hints: dict
    param_types: tuple  # Cached parameter types for quick checking

    def __init__(self, func: Callable, sig: Any, type_hints: dict, param_types: tuple):
        self.func = func
        self.sig = sig
        self.type_hints = type_hints
        self.param_types = param_types