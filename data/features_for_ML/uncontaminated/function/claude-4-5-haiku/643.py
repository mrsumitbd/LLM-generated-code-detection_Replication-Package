def _serialize_file_source(
    file_source: FileSource, context: SerdeContext
) -> LogicalPlanProto:
    """Serialize a file source (wrapper)."""
    from datafusion_expr import FileSource as FileSourceProto
    
    proto = LogicalPlanProto()
    proto.file_source.CopyFrom(
        FileSourceProto(
            path=file_source.path,
            file_type=file_source.file_type,
            projection=file_source.projection if file_source.projection else None,
            filters=[
                _serialize_expr(f, context) for f in file_source.filters
            ] if file_source.filters else [],
            limit=file_source.limit if file_source.limit else None,
            statistics=_serialize_statistics(file_source.statistics, context)
            if file_source.statistics else None,
        )
    )
    return proto