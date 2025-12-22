from typing import Callable, TypeVar, ParamSpec

P = ParamSpec("P")
T = TypeVar("T")

def wrapper(wrapped: Callable[P, T], instance: "Editable", args, kwargs) -> T:
    """
    Call the wrapped function with the given instance as the first argument.
    If the instance is None (method accessed via the class), call the function
    without the instance.
    """
    if instance is None:
        return wrapped(*args, **kwargs)  # type: ignore[arg-type]
    return wrapped(instance, *args, **kwargs)  # type: ignore[arg-type]