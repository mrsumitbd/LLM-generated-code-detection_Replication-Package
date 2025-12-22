def _serialize_file_source(
    file_source: FileSource, context: SerdeContext
) -> LogicalPlanProto:
    """Serialize a file source (wrapper)."""
    file_source_proto = LogicalPlanProto.FileSource()
    file_source_proto.path = file_source.path
    file_source_proto.format = file_source.format
    file_source_proto.options.update(file_source.options)
    file_source_proto.partition_keys.extend(file_source.partition_keys)
    file_source_proto.schema.CopyFrom(context.serialize_schema(file_source.schema))
    return LogicalPlanProto(file_source=file_source_proto)