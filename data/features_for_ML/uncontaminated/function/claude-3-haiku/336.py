def decorator(func: Callable):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result
    return wrapper