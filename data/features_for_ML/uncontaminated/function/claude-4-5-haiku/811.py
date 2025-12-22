def _parse_ast_node(node: ast.AST) -> Any:
    if isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.Str):
        return node.s
    elif isinstance(node, ast.Bytes):
        return node.s
    elif isinstance(node, ast.NameConstant):
        return node.value
    elif isinstance(node, ast.Ellipsis):
        return ...
    elif isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.List):
        return [_parse_ast_node(elt) for elt in node.elts]
    elif isinstance(node, ast.Tuple):
        return tuple(_parse_ast_node(elt) for elt in node.elts)
    elif isinstance(node, ast.Set):
        return {_parse_ast_node(elt) for elt in node.elts}
    elif isinstance(node, ast.Dict):
        return {_parse_ast_node(k): _parse_ast_node(v) for k, v in zip(node.keys, node.values)}
    elif isinstance(node, ast.UnaryOp):
        operand = _parse_ast_node(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +operand
        elif isinstance(node.op, ast.USub):
            return -operand
        elif isinstance(node.op, ast.Not):
            return not operand
        elif isinstance(node.op, ast.Invert):
            return ~operand
    elif isinstance(node, ast.BinOp):
        left = _parse_ast_node(node.left)
        right = _parse_ast_node(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        elif isinstance(node.op, ast.Sub):
            return left - right
        elif isinstance(node.op, ast.Mult):
            return left * right
        elif isinstance(node.op, ast.Div):
            return left / right
        elif isinstance(node.op, ast.FloorDiv):
            return left // right
        elif isinstance(node.op, ast.Mod):
            return left % right
        elif isinstance(node.op, ast.Pow):
            return left ** right
        elif isinstance(node.op, ast.LShift):
            return left << right
        elif isinstance(node.op, ast.RShift):
            return left >> right
        elif isinstance(node.op, ast.BitOr):
            return left | right
        elif isinstance(node.op, ast.BitXor):
            return left ^ right
        elif isinstance(node.op, ast.BitAnd):
            return left & right
    elif isinstance(node, ast.BoolOp):
        values = [_parse_ast_node(v) for v in node.values]
        if isinstance(node.op, ast.And):
            result = values[0]
            for v in values[1:]:
                result = result and v
            return result
        elif isinstance(node.op, ast.Or):
            result = values[0]
            for v in values[1:]:
                result = result or v
            return result
    elif isinstance(node, ast.Compare):
        left = _parse_ast_node(node.left)
        result = True
        for op, comparator in zip(node.ops, node.comparators):
            right = _parse_ast_node(comparator)
            if isinstance(op, ast.Eq):
                result = result and (left == right)
            elif isinstance(op, ast.NotEq):
                result = result and (left != right)
            elif isinstance(op, ast.Lt):
                result = result and (left < right)
            elif isinstance(op, ast.LtE):
                result = result and (left <= right)
            elif isinstance(op, ast.Gt):
                result = result and (left > right)
            elif isinstance(op, ast.GtE):
                result = result and (left >= right)
            elif isinstance(op, ast.Is):
                result = result and (left is right)
            elif isinstance(op, ast.IsNot):
                result = result and (left is not right)
            elif isinstance(op, ast.In):
                result = result and (left in right)
            elif isinstance(op, ast.NotIn):
                result = result and (left not in right)
            left = right
        return result
    elif isinstance(node, ast.IfExp):
        test = _parse_ast_node(node.test)
        if test:
            return _parse_ast_node(node.body)
        else:
            return _parse_ast_node(node.orelse)
    elif isinstance(node, ast.Lambda):
        return node
    elif isinstance(node, ast.Call):
        return node
    else:
        return node