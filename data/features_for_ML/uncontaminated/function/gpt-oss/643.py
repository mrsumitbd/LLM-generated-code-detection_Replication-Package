def _serialize_file_source(
    file_source: FileSource, context: SerdeContext
) -> LogicalPlanProto:
    """Serialize a file source (wrapper)."""
    # Create a new logical plan proto and set its type to FILE_SOURCE
    proto = LogicalPlanProto()
    proto.type = LogicalPlanProto.Type.FILE_SOURCE

    # Populate the file source specific fields.  Use getattr to be tolerant of
    # missing attributes – this allows the function to work with a variety of
    # FileSource implementations.
    file_source_proto = proto.file_source

    # Path
    if hasattr(file_source, "path"):
        file_source_proto.path = file_source.path

    # Format
    if hasattr(file_source, "format"):
        file_source_proto.format = file_source.format

    # Options – assume a mapping of key/value strings
    if hasattr(file_source, "options"):
        options = file_source.options
        if isinstance(options, dict):
            for k, v in options.items():
                file_source_proto.options[k] = v

    # Partition columns – assume an iterable of strings
    if hasattr(file_source, "partition_columns"):
        for col in file_source.partition_columns:
            file_source_proto.partition_columns.append(col)

    # Schema – use the context to serialize the schema if present
    if hasattr(file_source, "schema") and file_source.schema is not None:
        file_source_proto.schema.CopyFrom(context.serialize_schema(file_source.schema))

    return proto