def _deserialize_arithmetic_expr(
    logical_proto: ArithmeticExprProto, context: SerdeContext
) -> ArithmeticExpr:
    """Deserialize an arithmetic expression."""
    expr_type = logical_proto.WhichOneof("expr")
    if expr_type == "binary_expr":
        binary_expr = logical_proto.binary_expr
        left = _deserialize_arithmetic_expr(binary_expr.left, context)
        right = _deserialize_arithmetic_expr(binary_expr.right, context)
        operator = BinaryOperator(binary_expr.operator)
        return BinaryExpr(left, operator, right)
    elif expr_type == "unary_expr":
        unary_expr = logical_proto.unary_expr
        operand = _deserialize_arithmetic_expr(unary_expr.operand, context)
        operator = UnaryOperator(unary_expr.operator)
        return UnaryExpr(operator, operand)
    elif expr_type == "literal_expr":
        literal_expr = logical_proto.literal_expr
        value = context.deserialize_literal(literal_expr.value)
        return LiteralExpr(value)
    elif expr_type == "variable_expr":
        variable_expr = logical_proto.variable_expr
        name = variable_expr.name
        return VariableExpr(name)
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")