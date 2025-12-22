from typing import Callable

P = type(None)
T = type(None)

def wrapper(wrapped: Callable[[P], T], instance: "Editable", args, kwargs) -> T:
    return wrapped(*args, **kwargs)