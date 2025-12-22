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

def _get_spark_pool_id(container: VirtualItemContainer, spark_pool_name: str) -> str:
    ws_spark_pools = get_spark_pools(container)
    for sp in ws_spark_pools:
        if sp.name == spark_pool_name:
            return sp.id
    return None