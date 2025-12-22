def dispatcher(*args: Any, **kwargs: Any) -> Any:
    if args:
        return args[0]
    elif kwargs:
        return kwargs.get('default', None)
    else:
        return None