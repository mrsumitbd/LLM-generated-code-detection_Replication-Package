def handle_launch_config(node: ast.Call, context: ParseContext) -> dict:
    config = {}
    for keyword in node.keywords:
        config[keyword.arg] = keyword.value
    return config