from typing import Callable, Any

def decorator(func: Callable[..., Any]) -> Callable:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)
    return wrapper