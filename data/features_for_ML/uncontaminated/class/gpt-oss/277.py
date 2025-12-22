from __future__ import annotations

from typing import Any, Callable, Dict, Tuple, get_type_hints
import inspect


class Implementation:
    """
    A lightweight wrapper around a callable that keeps its signature,
    type hints and parameter types.  The wrapper can be called like the
    original function, but will perform a basic runtime type check
    against the stored type hints.
    """

    def __init__(
        self,
        func: Callable,
        sig: Any,
        type_hints: Dict[str, Any],
        param_types: Tuple[type, ...],
    ) -> None:
        self.func = func
        self.sig = sig
        self.type_hints = type_hints
        self.param_types = param_types

    @classmethod
    def from_callable(cls, func: Callable) -> "Implementation":
        """
        Convenience constructor that automatically extracts the signature,
        type hints and parameter types from a callable.
        """
        sig = inspect.signature(func)
        type_hints = get_type_hints(func)
        param_types = tuple(
            type_hints.get(name, Any) for name in sig.parameters
        )
        return cls(func, sig, type_hints, param_types)

    def __call__(self, *args, **kwargs):
        """
        Call the wrapped function after performing a simple runtime type
        check against the stored type hints.
        """
        bound = self.sig.bind_partial(*args, **kwargs)
        bound.apply_defaults()

        for name, value in bound.arguments.items():
            expected = self.type_hints.get(name)
            if expected is not None and expected is not Any:
                if not isinstance(value, expected):
                    raise TypeError(
                        f"Argument '{name}' expected type {expected.__name__}, "
                        f"got {type(value).__name__}"
                    )

        return self.func(*bound.args, **bound.kwargs)

    def __repr__(self) -> str:
        return (
            f"<Implementation func={self.func.__name__!r} "
            f"sig={self.sig} type_hints={self.type_hints}>"
        )