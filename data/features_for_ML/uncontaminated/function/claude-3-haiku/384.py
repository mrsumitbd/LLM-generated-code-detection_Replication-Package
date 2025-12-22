def decorator(inner_func: Callable):
    def wrapper(*args, **kwargs):
        result = inner_func(*args, **kwargs)
        return result
    return wrapper