import ast
import operator
from typing import Any

# Mapping of AST operator nodes to actual Python operators
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.MatMult: operator.matmul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.LShift: operator.lshift,
    ast.RShift: operator.rshift,
    ast.BitOr: operator.or_,
    ast.BitXor: operator.xor,
    ast.BitAnd: operator.and_,
}

_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
    ast.Not: operator.not_,
    ast.Invert: operator.invert,
}

_BOOL_OPS = {
    ast.And: all,
    ast.Or: any,
}

_COMPARE_OPS = {
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
    ast.Is: operator.is_,
    ast.IsNot: operator.is_not,
    ast.In: operator.contains,
    ast.NotIn: lambda a, b: not operator.contains(a, b),
}

def _parse_ast_node(node: ast.AST) -> Any:
    """
    Recursively convert an AST node into a Python value.
    Supports literals, collections, unary/binary ops, bool ops, and comparisons.
    Raises ValueError for unsupported nodes.
    """
    if node is None:
        return None

    # Constants (Python 3.8+)
    if isinstance(node, ast.Constant):
        return node.value

    # Legacy constants (Python <3.8)
    if isinstance(node, ast.Num):
        return node.n
    if isinstance(node, ast.Str):
        return node.s
    if isinstance(node, ast.Bytes):
        return node.s
    if isinstance(node, ast.NameConstant):
        return node.value

    # Names: only allow True, False, None
    if isinstance(node, ast.Name):
        if node.id == "True":
            return True
        if node.id == "False":
            return False
        if node.id == "None":
            return None
        raise ValueError(f"Unsupported name: {node.id}")

    # Collections
    if isinstance(node, ast.Tuple):
        return tuple(_parse_ast_node(e) for e in node.elts)
    if isinstance(node, ast.List):
        return [_parse_ast_node(e) for e in node.elts]
    if isinstance(node, ast.Set):
        return {_parse_ast_node(e) for e in node.elts}
    if isinstance(node, ast.Dict):
        return {_parse_ast_node(k): _parse_ast_node(v) for k, v in zip(node.keys, node.values)}

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type in _UNARY_OPS:
            operand = _parse_ast_node(node.operand)
            return _UNARY_OPS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    # Binary operations
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type in _BIN_OPS:
            left = _parse_ast_node(node.left)
            right = _parse_ast_node(node.right)
            return _BIN_OPS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    # Boolean operations
    if isinstance(node, ast.BoolOp):
        op_type = type(node.op)
        if op_type in _BOOL_OPS:
            values = [_parse_ast_node(v) for v in node.values]
            # For 'and' and 'or', we need short-circuit semantics
            if op_type is ast.And:
                for v in values:
                    if not v:
                        return False
                return True
            if op_type is ast.Or:
                for v in values:
                    if v:
                        return True
                return False
        raise ValueError(f"Unsupported boolean operator: {op_type.__name__}")

    # Comparisons
    if isinstance(node, ast.Compare):
        left = _parse_ast_node(node.left)
        for op, comparator in zip(node.ops, node.comparators):
            op_type = type(op)
            if op_type in _COMPARE_OPS:
                right = _parse_ast_node(comparator)
                if not _COMPARE_OPS[op_type](left, right):
                    return False
                left = right
            else:
                raise ValueError(f"Unsupported comparison operator: {op_type.__name__}")
        return True

    # If we reach here, the node type is unsupported
    raise ValueError(f"Unsupported AST node type: {type(node).__name__}")