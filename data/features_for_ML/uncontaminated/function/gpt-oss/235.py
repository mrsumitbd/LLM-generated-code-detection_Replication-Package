import ast
from typing import List

def validate_expression(expression: str, allowed_keys: List[str]) -> None:
    """
    Validate that a Python expression string only contains identifiers from
    `allowed_keys` and does not use any disallowed syntax such as attribute
    access, function calls, imports, or other potentially unsafe constructs.

    Parameters
    ----------
    expression : str
        The expression to validate.
    allowed_keys : list[str]
        A list of identifier names that are permitted to appear in the
        expression.

    Raises
    ------
    ValueError
        If the expression cannot be parsed, or if it contains disallowed
        identifiers or syntax.
    """
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from exc

    # Helper to recursively walk the AST
    def _walk(node: ast.AST):
        for child in ast.iter_child_nodes(node):
            # Disallow attribute access (e.g., obj.attr)
            if isinstance(child, ast.Attribute):
                raise ValueError(
                    f"Attribute access is not allowed: {ast.dump(child)}"
                )
            # Disallow function calls
            if isinstance(child, ast.Call):
                raise ValueError(
                    f"Function calls are not allowed: {ast.dump(child)}"
                )
            # Disallow imports or import-from nodes
            if isinstance(child, (ast.Import, ast.ImportFrom)):
                raise ValueError(
                    f"Import statements are not allowed: {ast.dump(child)}"
                )
            # Disallow lambda expressions
            if isinstance(child, ast.Lambda):
                raise ValueError(
                    f"Lambda expressions are not allowed: {ast.dump(child)}"
                )
            # Disallow comprehensions (list/set/dict/generator)
            if isinstance(child, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
                raise ValueError(
                    f"Comprehensions are not allowed: {ast.dump(child)}"
                )
            # Disallow subscript access (e.g., a[0])
            if isinstance(child, ast.Subscript):
                raise ValueError(
                    f"Subscript access is not allowed: {ast.dump(child)}"
                )
            # Disallow assignment or augmented assignment
            if isinstance(child, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
                raise ValueError(
                    f"Assignment is not allowed: {ast.dump(child)}"
                )
            # Disallow delete statements
            if isinstance(child, ast.Delete):
                raise ValueError(
                    f"Delete statements are not allowed: {ast.dump(child)}"
                )
            # Disallow if, while, for, try, with, etc.
            if isinstance(child, (ast.If, ast.While, ast.For, ast.Try, ast.With)):
                raise ValueError(
                    f"Control flow statements are not allowed: {ast.dump(child)}"
                )
            # Check identifier usage
            if isinstance(child, ast.Name):
                if child.id not in allowed_keys:
                    raise ValueError(
                        f"Identifier '{child.id}' is not in the list of allowed keys."
                    )
            # Recurse into child nodes
            _walk(child)

    _walk(tree)