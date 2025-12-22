def _deserialize_json_contains_expr(
    logical_proto: JsonContainsExprProto, context: SerdeContext
) -> JsonContainsExpr:
    json_expr = deserialize_expression(logical_proto.json_expr, context)
    pattern_expr = deserialize_expression(logical_proto.pattern_expr, context)
    return JsonContainsExpr(json_expr, pattern_expr)