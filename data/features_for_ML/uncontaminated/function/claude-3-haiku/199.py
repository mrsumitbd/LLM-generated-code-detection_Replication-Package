def extract_type_arg(typ: type, index: int) -> type:
    """
    Extracts the type argument at the specified index from the given type.

    Args:
        typ (type): The type from which to extract the type argument.
        index (int): The index of the type argument to extract.

    Returns:
        type: The extracted type argument.
    """
    if not hasattr(typ, "__args__"):
        raise TypeError(f"{typ} is not a generic type.")
    if len(typ.__args__) <= index:
        raise IndexError(f"Index {index} is out of range for type {typ}.")
    return typ.__args__[index]