def dispatcher(*args: Any, **kwargs: Any) -> Any:
    # Quick path: try direct positional args match first
    key = tuple(type(arg) for arg in args)
    
    if key in registry:
        return registry[key](*args, **kwargs)
    
    # Fallback: try to find a matching implementation
    for registered_key, func in registry.items():
        if len(registered_key) == len(args):
            if all(isinstance(arg, registered_type) 
                   for arg, registered_type in zip(args, registered_key)):
                return func(*args, **kwargs)
    
    # No matching implementation found
    raise NotImplementedError(
        f"No implementation found for types: {key}"
    )