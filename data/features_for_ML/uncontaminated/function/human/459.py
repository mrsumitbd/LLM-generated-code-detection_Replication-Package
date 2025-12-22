from fabric_cli.core.fab_exceptions import FabricCLIError
from fabric_cli.core.hiearchy.fab_hiearchy import (
    ExternalDataShareVirtualItem,
    Folder,
    Item,
    Tenant,
    VirtualItem,
    VirtualItemContainer,
    VirtualWorkspaceItem,
    Workspace,
)
from fabric_cli.core import fab_constant, fab_logger
from fabric_cli.errors import ErrorMessages

def get_spark_pool_id(container: VirtualItemContainer, name) -> str:
    spark_pool_name = name.strip("/")
    spark_pool_id = _get_spark_pool_id(container, spark_pool_name)

    # if not found, invalidate the cache and try again
    if spark_pool_id is None:
        _get_spark_pools_from_cache.cache.clear()
        spark_pool_id = _get_spark_pool_id(container, spark_pool_name)

    if spark_pool_id:
        return spark_pool_id

    raise FabricCLIError(
        ErrorMessages.Common.resource_not_found({"type": "Spark Pool", "name": name}),
        fab_constant.ERROR_NOT_FOUND,
    )