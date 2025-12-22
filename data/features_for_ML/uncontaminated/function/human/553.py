from typing import (TypeVar, Callable, get_type_hints, overload as typing_overload,
                    Any, Type, Union, get_args, get_origin, cast)
from .function_isolation import isolate_function

def dispatcher(*args: Any, **kwargs: Any) -> Any:
            # Quick path: try direct positional args match first
            if not kwargs:
                for impl in _registry[qualname]:
                    if len(args) == len(impl.param_types):
                        if all(_check_type(arg, type_)
                               for arg, (_, type_) in zip(args, impl.param_types)):
                            return isolate_function(impl.func, '__overloaded__', __scope_id__)(*args)

            # Slower path: handle mixed args/kwargs
            for impl in _registry[qualname]:
                try:
                    bound = impl.sig.bind(*args, **kwargs)
                    bound.apply_defaults()

                    if all(_check_type(value, impl.type_hints.get(name, Any))
                           for name, value in bound.arguments.items()):
                        return isolate_function(impl.func, '__overloaded__', __scope_id__)(*args, **kwargs)
                except TypeError:
                    continue

            raise TypeError(f"No matching implementation found for {qualname}: {args}, {kwargs}")