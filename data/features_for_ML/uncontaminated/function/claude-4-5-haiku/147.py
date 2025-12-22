def wrapper(wrapped: Callable[P, T], instance: "Editable", args, kwargs) -> T:
    if instance is None:
        return wrapped(*args, **kwargs)
    
    if not instance._editable:
        raise RuntimeError(f"Cannot call {wrapped.__name__} on non-editable instance")
    
    return wrapped(instance, *args, **kwargs)