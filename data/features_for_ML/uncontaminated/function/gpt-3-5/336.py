def decorator(func: Callable):
    def wrapper(*args, **kwargs):
        # Add your custom code here
        result = func(*args, **kwargs)
        # Add your custom code here
        return result
    return wrapper