import ast
from typing import Optional

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
    # Ensure we are dealing with a Call node
    if not isinstance(call_node, ast.Call):
        return None

    # Iterate over keyword arguments
    for kw in call_node.keywords:
        # kw.arg is None for **kwargs; skip those
        if kw.arg == keyword_name:
            return kw.value

    # Keyword not found
    return None