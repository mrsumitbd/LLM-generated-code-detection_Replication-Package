from typing import Any, Dict, List, Optional, Tuple, Union, Literal
import ast

def _parse_ast_node(node: ast.AST) -> Any:
            if isinstance(node, ast.Constant):
                return node.value
            elif isinstance(node, ast.List):
                return [_parse_ast_node(elt) for elt in node.elts]
            elif isinstance(node, ast.Tuple):
                return tuple(_parse_ast_node(elt) for elt in node.elts)
            elif isinstance(node, ast.Dict):
                return { _parse_ast_node(key): _parse_ast_node(value) for key, value in zip(node.keys, node.values) }
            elif isinstance(node, ast.UnaryOp):
                if isinstance(node.op, ast.USub):
                    return -_parse_ast_node(node.operand)
                elif isinstance(node.op, ast.UAdd):
                    return _parse_ast_node(node.operand)
                else:
                    raise TypeError(f"Unsupported unary operator: {type(node.op)}")
            else:
                raise TypeError(f"Unsupported AST node type: {type(node)}")