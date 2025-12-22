def _serialize_split_part_expr(
    logical: SplitPartExpr, context: SerdeContext
) -> LogicalExprProto:
    """Serialize a split part expression."""
    from datafusion_expr_pb2 import LogicalExprProto, SplitPartExpr as SplitPartExprProto
    
    split_part_proto = SplitPartExprProto()
    split_part_proto.expr.CopyFrom(_serialize_expr(logical.expr, context))
    split_part_proto.delimiter.CopyFrom(_serialize_expr(logical.delimiter, context))
    split_part_proto.index.CopyFrom(_serialize_expr(logical.index, context))
    
    result = LogicalExprProto()
    result.split_part.CopyFrom(split_part_proto)
    return result