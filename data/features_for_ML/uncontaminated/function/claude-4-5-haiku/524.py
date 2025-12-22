def decorator(obj):
    def wrapper(*args, **kwargs):
        result = obj(*args, **kwargs)
        return result
    return wrapper