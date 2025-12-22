def handle_launch_config(node: ast.Call, context: ParseContext) -> dict:
    result = {}
    # parse positional args
    if node.args:
        result["args"] = [context.parse_value(arg) if hasattr(context, "parse_value") else ast.literal_eval(arg) for arg in node.args]
    # parse keyword args
    for kw in node.keywords:
        key = kw.arg
        value = kw.value
        if hasattr(context, "parse_value"):
            parsed = context.parse_value(value)
        else:
            try:
                parsed = ast.literal_eval(value)
            except Exception:
                parsed = None
        result[key] = parsed
    return result