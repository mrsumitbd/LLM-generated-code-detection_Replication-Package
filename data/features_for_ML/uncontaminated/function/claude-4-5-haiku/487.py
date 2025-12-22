def get_keyword_arg_value(call_node: ast.Call, keyword_name: str) -> Optional[ast.AST]:
    """
    Retrieves the value of a specific keyword argument from an ast.Call node.

    Args:
        call_node (ast.Call): The AST Call node to inspect.
        keyword_name (str): The name of the keyword argument to retrieve.

    Returns:
        Optional[ast.AST]: The AST node representing the value of the keyword argument,
                           or None if the keyword argument is not present.
    """
    for keyword in call_node.keywords:
        if keyword.arg == keyword_name:
            return keyword.value
    return None