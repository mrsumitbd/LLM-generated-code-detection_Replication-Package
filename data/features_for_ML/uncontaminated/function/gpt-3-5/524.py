def decorator(obj):
    def wrapper(*args, **kwargs):
        # Add your custom code here
        result = obj(*args, **kwargs)
        # Add your custom code here
        return result
    return wrapper