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

def get_folder(workspace: Workspace, id: str) -> Folder:
    ws_folders = get_workspace_folders(workspace)
    for folder in ws_folders:
        if folder.id == id:
            return folder
    return None