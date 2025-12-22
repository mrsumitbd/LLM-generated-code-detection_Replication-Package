def run(*args, **kwargs):
    if not args:
        return None
    func = args[0]
    if callable(func):
        return func(*args[1:], **kwargs)
    return args, kwargs