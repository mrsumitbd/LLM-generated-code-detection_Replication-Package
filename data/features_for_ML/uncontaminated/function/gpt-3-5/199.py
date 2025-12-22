def extract_type_arg(typ: type, index: int) -> type:
    if hasattr(typ, '__args__') and typ.__args__ is not None:
        if 0 <= index < len(typ.__args__):
            return typ.__args__[index]
    return None