def _deserialize_equality_comparison_expr(
    logical_proto: EqualityComparisonExprProto, context: SerdeContext
) -> EqualityComparisonExpr:
    """Deserialize an equality comparison expression."""
    left = _deserialize_expression(logical_proto.left, context)
    right = _deserialize_expression(logical_proto.right, context)
    operator = logical_proto.operator

    return EqualityComparisonExpr(left, operator, right)