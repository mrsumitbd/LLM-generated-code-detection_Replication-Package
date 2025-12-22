from typing import Any, Callable, Dict, Tuple

# Global registry mapping a tuple of argument types to a callable
_dispatch_registry: Dict[Tuple[type, ...], Callable[..., Any]] = {}

def register(*types: type) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to register a function for a specific tuple of argument types.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        _dispatch_registry[types] = func
        return func
    return decorator

def dispatcher(*args: Any, **kwargs: Any) -> Any:
    """
    Dispatches a call to a registered function based on the runtime types of
    the positional arguments.

    Quick path: try direct positional args match first.
    """
    # Quick path: try direct positional args match first
    types = tuple(type(arg) for arg in args)
    if types in _dispatch_registry:
        return _dispatch_registry[types](*args, **kwargs)

    # Fallback: try to find a match where each argument is an instance of the
    # registered type (allowing subclasses).
    for key, func in _dispatch_registry.items():
        if len(key) != len(args):
            continue
        if all(isinstance(arg, typ) for arg, typ in zip(args, key)):
            return func(*args, **kwargs)

    # No match found – raise an informative error
    raise TypeError(f"No matching function for argument types {types}")