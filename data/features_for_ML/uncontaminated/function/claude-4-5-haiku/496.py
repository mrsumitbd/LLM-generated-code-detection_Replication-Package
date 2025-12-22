def decorator(handler: RouteHandler):
    def wrapper(*args, **kwargs):
        return handler(*args, **kwargs)
    return wrapper