def decorator(kernel_fn):
    def wrapper(*args, **kwargs):
        # Add your custom code here
        result = kernel_fn(*args, **kwargs)
        # Add your custom code here
        return result
    return wrapper