def _deserialize_arithmetic_expr(logical_proto: ArithmeticExprProto, context: SerdeContext) -> ArithmeticExpr:
    arithmetic_expr = ArithmeticExpr()
    arithmetic_expr.op = logical_proto.op
    if logical_proto.HasField("lhs"):
        arithmetic_expr.lhs = _deserialize_arithmetic_expr(logical_proto.lhs, context)
    if logical_proto.HasField("rhs"):
        arithmetic_expr.rhs = _deserialize_arithmetic_expr(logical_proto.rhs, context)
    return arithmetic_expr