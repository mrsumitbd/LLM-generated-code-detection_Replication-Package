def _deserialize_equality_comparison_expr(
    logical_proto: EqualityComparisonExprProto, context: SerdeContext
) -> EqualityComparisonExpr:
    """Deserialize an equality comparison expression."""
    left = _deserialize_expr(logical_proto.left, context)
    right = _deserialize_expr(logical_proto.right, context)
    operator = EqualityComparisonOperator(logical_proto.operator)
    return EqualityComparisonExpr(left=left, right=right, operator=operator)