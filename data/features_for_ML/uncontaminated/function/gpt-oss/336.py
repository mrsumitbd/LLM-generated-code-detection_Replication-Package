from typing import Callable

def decorator(func: Callable):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper