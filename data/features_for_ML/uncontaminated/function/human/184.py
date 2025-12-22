from typing import Optional
from fabric_cli.core.hiearchy.fab_hiearchy import (
    FabricElement,
    Item,
    LocalPath,
    OneLakeItem,
    Tenant,
    VirtualItem,
    VirtualItemContainer,
    VirtualWorkspace,
    VirtualWorkspaceItem,
    Workspace,
)
from fabric_cli.core import fab_constant, fab_logger
from fabric_cli.core.fab_exceptions import FabricCLIError
from fabric_cli.utils import fab_mem_store as mem_store

def _get_gateway_id(
    tenant: Tenant, gateway_name: str, raise_error: bool = True
) -> Optional[str]:
    try:
        gateway_id = mem_store.get_gateway_id(tenant, gateway_name)
    except FabricCLIError as e:
        if not (raise_error) and e.status_code == fab_constant.ERROR_NOT_FOUND:
            gateway_id = None
        else:
            raise e

    return gateway_id