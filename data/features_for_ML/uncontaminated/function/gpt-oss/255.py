def _serialize_split_part_expr(
    logical: SplitPartExpr, context: SerdeContext
) -> LogicalExprProto:
    """Serialize a split part expression."""
    # Create the top‑level logical expression proto
    proto = LogicalExprProto()
    proto.type = LogicalExprProto.Type.SPLIT_PART_EXPR

    # Populate the split part specific fields
    split_proto = proto.split_part_expr
    split_proto.expr.CopyFrom(context.serialize_expr(logical.expr))
    split_proto.delimiter = logical.delimiter
    split_proto.part = logical.part

    return proto