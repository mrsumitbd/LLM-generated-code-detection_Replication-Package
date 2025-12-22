def _serialize_file_source(
    file_source: FileSource, context: SerdeContext
) -> LogicalPlanProto:
    logical_plan_proto = LogicalPlanProto()
    logical_plan_proto.file_source.CopyFrom(file_source.to_proto())
    logical_plan_proto.serde_context.CopyFrom(context.to_proto())
    return logical_plan_proto