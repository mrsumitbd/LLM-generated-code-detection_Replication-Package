import functools

def decorator(obj):
    @functools.wraps(obj)
    def wrapper(*args, **kwargs):
        return obj(*args, **kwargs)
    return wrapper