def parse_as_attr(arg: str) -> Arg:
    if not isinstance(arg, str):
        raise TypeError(f"Expected a string, got {type(arg).__name__}")
    if "=" not in arg:
        raise ValueError(f"Argument '{arg}' is not in key=value format")
    name, value = arg.split("=", 1)
    return Arg(name=name.strip(), value=value.strip())