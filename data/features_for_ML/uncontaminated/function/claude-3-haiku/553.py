def dispatcher(*args: Any, **kwargs: Any) -> Any:
    # Quick path: try direct positional args match first
    try:
        return args[0](*args[1:], **kwargs)
    except (IndexError, TypeError):
        pass

    # Try to find a matching function in the kwargs
    for key, value in kwargs.items():
        if callable(value):
            try:
                return value(*args, **kwargs)
            except TypeError:
                pass

    # If no match found, return None
    return None