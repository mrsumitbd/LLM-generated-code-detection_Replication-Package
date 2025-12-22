def _deserialize_arithmetic_expr(
    logical_proto: ArithmeticExprProto, context: SerdeContext
) -> ArithmeticExpr:
    """Deserialize an arithmetic expression."""
    operator = logical_proto.operator
    left = _deserialize_expr(logical_proto.left, context)
    right = _deserialize_expr(logical_proto.right, context)
    return ArithmeticExpr(operator=operator, left=left, right=right)