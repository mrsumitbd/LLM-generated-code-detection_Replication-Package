import ast
from typing import Any

def _parse_ast_node(node: ast.AST) -> Any:
    if isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        return f"{_parse_ast_node(node.value)}.{node.attr}"
    elif isinstance(node, ast.Call):
        return f"{_parse_ast_node(node.func)}({', '.join(_parse_ast_node(arg) for arg in node.args)})"
    elif isinstance(node, ast.List):
        return f"[{', '.join(_parse_ast_node(item) for item in node.elts)}]"
    elif isinstance(node, ast.Tuple):
        return f"({', '.join(_parse_ast_node(item) for item in node.elts)})"
    elif isinstance(node, ast.Dict):
        return f"{{{', '.join(_parse_ast_node(key) + ': ' + _parse_ast_node(value) for key, value in zip(node.keys, node.values))}}}"
    elif isinstance(node, ast.BinOp):
        return f"({_parse_ast_node(node.left)} {type(node.op).__name__} {_parse_ast_node(node.right)})"
    elif isinstance(node, ast.UnaryOp):
        return f"({type(node.op).__name__} {_parse_ast_node(node.operand)})"
    elif isinstance(node, ast.Compare):
        return f"({_parse_ast_node(node.left)} {' '.join(type(op).__name__ for op in node.ops)} {' '.join(_parse_ast_node(comp) for comp in node.comparators)})"
    elif isinstance(node, ast.IfExp):
        return f"({_parse_ast_node(node.test)} if {_parse_ast_node(node.body)} else {_parse_ast_node(node.orelse)})"
    elif isinstance(node, ast.ListComp):
        return f"[{_parse_ast_node(node.elt)} for {', '.join(_parse_ast_node(generator) for generator in node.generators)}]"
    elif isinstance(node, ast.GeneratorExp):
        return f"({_parse_ast_node(node.elt)} for {', '.join(_parse_ast_node(generator) for generator in node.generators)})"
    elif isinstance(node, ast.comprehension):
        return f"{_parse_ast_node(node.target)} in {_parse_ast_node(node.iter)}"
    else:
        return repr(node)