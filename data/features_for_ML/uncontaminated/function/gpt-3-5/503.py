def _deserialize_equality_comparison_expr(logical_proto: EqualityComparisonExprProto, context: SerdeContext) -> EqualityComparisonExpr:
    return EqualityComparisonExpr(
        left=_deserialize_expr(logical_proto.left, context),
        right=_deserialize_expr(logical_proto.right, context),
        op=logical_proto.op,
    )