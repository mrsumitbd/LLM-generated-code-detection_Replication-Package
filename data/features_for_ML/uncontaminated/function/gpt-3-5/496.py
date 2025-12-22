def decorator(handler: RouteHandler):
    def wrapper(*args, **kwargs):
        # Do something before calling the handler
        result = handler(*args, **kwargs)
        # Do something after calling the handler
        return result
    return wrapper