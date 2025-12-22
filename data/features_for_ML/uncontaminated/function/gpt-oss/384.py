import functools
from typing import Callable

def decorator(inner_func: Callable):
    @functools.wraps(inner_func)
    def wrapper(*args, **kwargs):
        return inner_func(*args, **kwargs)
    return wrapper