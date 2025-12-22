def decorator(handler: RouteHandler):
    def wrapper(*args, **kwargs):
        # Perform pre-processing logic here
        result = handler(*args, **kwargs)
        # Perform post-processing logic here
        return result
    return wrapper