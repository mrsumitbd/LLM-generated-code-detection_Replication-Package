def _serialize_split_part_expr(logical: SplitPartExpr, context: SerdeContext) -> LogicalExprProto:
    proto = LogicalExprProto()
    proto.split_part_expr.CopyFrom(logical)
    return proto