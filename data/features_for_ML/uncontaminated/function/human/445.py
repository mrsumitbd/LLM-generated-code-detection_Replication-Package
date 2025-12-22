from typing import Annotated, Any, Literal, Union, get_args
from snowflake.core import CreateMode, Root
from mcp_server_snowflake.object_manager.objects import (
    SnowflakeComputePool,
    SnowflakeDatabase,
    SnowflakeImageRepository,
    SnowflakeObject,
    SnowflakeRole,
    SnowflakeSchema,
    SnowflakeStage,
    SnowflakeTable,
    SnowflakeUser,
    SnowflakeView,
    SnowflakeWarehouse,
    supported_objects,
)
from mcp_server_snowflake.utils import SnowflakeException, execute_query

def create_object(
    snowflake_object: SnowflakeObject,
    root: Root,
    mode: Literal["error_if_exists", "replace", "if_not_exists"] = "error_if_exists",
):
    if mode == "error_if_exists":
        create_mode = CreateMode.error_if_exists
    elif mode == "replace":
        create_mode = CreateMode.or_replace
    elif mode == "if_not_exists":
        create_mode = CreateMode.if_not_exists
    else:
        create_mode = CreateMode.if_not_exists
    core_object = snowflake_object.get_core_object()
    core_path = snowflake_object.get_core_path(root=root)
    try:
        core_path.create(core_object, mode=create_mode)
        return f"Created {get_class_name(core_object)} {core_object.name}."
    except Exception as e:
        raise SnowflakeException(tool="create_object", message=str(e))