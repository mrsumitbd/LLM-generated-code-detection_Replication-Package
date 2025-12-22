def parse_as_attr(arg: str) -> Arg:
    """Parse a string argument as an attribute access expression."""
    parts = arg.split('.')
    if not parts or not parts[0]:
        raise ValueError(f"Invalid attribute expression: {arg}")
    
    # First part should be a valid identifier
    obj = Arg(parts[0], 'name')
    
    # Process remaining parts as attribute accesses
    for part in parts[1:]:
        if not part or not part.isidentifier():
            raise ValueError(f"Invalid attribute name: {part}")
        obj = Arg(obj, 'getattr', part)
    
    return obj