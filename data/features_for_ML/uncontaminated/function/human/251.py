def parse_as_attr(arg: str) -> Arg:
    if _LONG_ARG.match(arg):
        return Arg(value=dash_to_snake(arg), orig=arg, arg_type="long-opt")

    if _SHORT_ARG.match(arg):
        return Arg(value=dash_to_snake(arg), orig=arg, arg_type="short-opt")

    return Arg(value=arg, orig=arg, arg_type="pos")