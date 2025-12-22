def _serialize_split_part_expr(
    logical: SplitPartExpr, context: SerdeContext
) -> LogicalExprProto:
    """Serialize a split part expression."""
    proto = LogicalExprProto()
    proto.split_part_expr.column = logical.column
    proto.split_part_expr.index = logical.index
    proto.split_part_expr.delimiter = logical.delimiter
    proto.split_part_expr.remove_empty = logical.remove_empty
    return proto