def wrapper(*args, **kwargs):  # type: ignore
    # If used as a decorator: wrapper(func)
    if len(args) == 1 and callable(args[0]) and not kwargs:
        func = args[0]

        def inner(*a, **kw):
            return func(*a, **kw)

        return inner
    # If called directly, just return the arguments
    return args, kwargs