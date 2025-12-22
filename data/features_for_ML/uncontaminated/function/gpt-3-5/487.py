def get_keyword_arg_value(call_node: ast.Call, keyword_name: str) -> Optional[ast.AST]:
    for keyword in call_node.keywords:
        if keyword.arg == keyword_name:
            return keyword.value
    return None