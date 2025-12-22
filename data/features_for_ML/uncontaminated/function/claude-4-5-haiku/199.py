def extract_type_arg(typ: type, index: int) -> type:
    import typing
    
    # Get the origin and args of the type
    origin = typing.get_origin(typ)
    args = typing.get_args(typ)
    
    # If there are no args, return the type itself
    if not args:
        return typ
    
    # Return the argument at the specified index
    if index < len(args):
        return args[index]
    
    # If index is out of range, raise an IndexError
    raise IndexError(f"Type argument index {index} out of range for type {typ}")