def _deserialize_json_contains_expr(logical_proto: JsonContainsExprProto, context: SerdeContext) -> JsonContainsExpr:
    return JsonContainsExpr(
        lhs=_deserialize_json_expr(logical_proto.lhs, context),
        rhs=_deserialize_json_expr(logical_proto.rhs, context)
    )