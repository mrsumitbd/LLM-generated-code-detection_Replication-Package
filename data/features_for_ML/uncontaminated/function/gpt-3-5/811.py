def _parse_ast_node(node: ast.AST) -> Any:
    if isinstance(node, ast.Module):
        return "Module"
    elif isinstance(node, ast.FunctionDef):
        return "FunctionDef"
    elif isinstance(node, ast.ClassDef):
        return "ClassDef"
    elif isinstance(node, ast.Assign):
        return "Assign"
    elif isinstance(node, ast.Expr):
        return "Expr"
    elif isinstance(node, ast.Call):
        return "Call"
    else:
        return "Unknown"