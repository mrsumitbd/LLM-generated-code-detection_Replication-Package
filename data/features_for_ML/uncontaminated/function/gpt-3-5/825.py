def get_folder(workspace: Workspace, id: str) -> Folder:
    for folder in workspace.folders:
        if folder.id == id:
            return folder
    return None