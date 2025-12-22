def decorator(kernel_fn):
    def wrapper(*args, **kwargs):
        result = kernel_fn(*args, **kwargs)
        return result
    return wrapper