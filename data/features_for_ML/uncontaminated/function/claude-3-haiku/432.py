def _deserialize_json_contains_expr(
    logical_proto: JsonContainsExprProto, context: SerdeContext
) -> JsonContainsExpr:
    path = _deserialize_json_path(logical_proto.path, context)
    value = _deserialize_json_value(logical_proto.value, context)
    return JsonContainsExpr(path, value)