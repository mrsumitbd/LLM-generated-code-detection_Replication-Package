from typing import Any, Callable

def decorator(handler: RouteHandler) -> Callable[..., Any]:
    """
    A simple decorator that forwards all arguments to the wrapped handler.
    """
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return handler(*args, **kwargs)

    return wrapper