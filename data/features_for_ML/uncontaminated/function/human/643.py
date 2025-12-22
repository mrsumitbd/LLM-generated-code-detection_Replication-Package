from fenic.core._logical_plan.plans.source import (
    DocSource,
    FileSource,
    InMemorySource,
    TableSource,
)
from fenic.core._serde.proto.serde_context import SerdeContext
from fenic.core._serde.proto.types import (
    DocContentTypeProto,
    DocSourceProto,
    FileSourceProto,
    InMemorySourceProto,
    LogicalPlanProto,
    TableSourceProto,
)

def _serialize_file_source(
    file_source: FileSource, context: SerdeContext
) -> LogicalPlanProto:
    """Serialize a file source (wrapper)."""
    if file_source._options:
        options_merge_schema = file_source._options.get("merge_schemas", None)
        options_schema = (
            context.serialize_fenic_schema(file_source._options.get("schema"))
            if file_source._options.get("schema", None) else None
        )
    else:
        options_merge_schema = None
        options_schema = None
    return LogicalPlanProto(
        file_source=FileSourceProto(
            paths=file_source._paths,
            file_format=file_source._file_format,
            options_merge_schema=options_merge_schema,
            options_schema=options_schema,
        )
    )