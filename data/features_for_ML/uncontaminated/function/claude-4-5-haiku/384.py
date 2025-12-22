def decorator(inner_func: Callable):
    def outer_func(*args, **kwargs):
        return inner_func(*args, **kwargs)
    return outer_func