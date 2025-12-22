def decorator(kernel_fn):
    def wrapper(*args, **kwargs):
        return kernel_fn(*args, **kwargs)
    return wrapper