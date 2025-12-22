def wrapper(model):
    def decorator(func):
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            return model(result)
        return inner
    return decorator