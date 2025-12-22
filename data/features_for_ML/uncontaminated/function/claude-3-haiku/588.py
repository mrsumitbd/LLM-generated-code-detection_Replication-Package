def handle_launch_config(node: ast.Call, context: ParseContext) -> dict:
    launch_config = {}
    for arg in node.args:
        if isinstance(arg, ast.Keyword):
            key = arg.arg
            value = context.evaluate(arg.value)
            launch_config[key] = value
        elif isinstance(arg, ast.Call):
            key, value = handle_launch_config(arg, context)
            launch_config.update(value)
    return launch_config