from typing import Annotated, Any, Literal, Union, get_args
from pydantic import Field

def list_objects_tool(
        object_type: object_type_annotation,
        database_name: str | None = None,
        schema_name: str | None = None,
        like: Annotated[
            str | None,
            Field(
                description="Filter objects by keyword in name. Uses case-insensitive pattern matching, with support for SQL wildcard characters (% and _).",
                default=None,
            ),
        ] = None,
        starts_with: Annotated[
            str | None,
            Field(
                description="Filter objects by start of name. Case sensitive. Ignored for warehouses.",
                default=None,
            ),
        ] = None,
    ):
        return list_objects(
            snowflake_service,
            object_type,
            database_name,
            schema_name,
            like,
            starts_with,
        )