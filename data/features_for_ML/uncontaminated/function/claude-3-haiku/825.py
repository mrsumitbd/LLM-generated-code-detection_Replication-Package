def get_folder(workspace: Workspace, id: str) -> Folder:
    try:
        folder = workspace.folders.get(id)
        if folder is None:
            raise ValueError(f"Folder with ID '{id}' not found in the workspace.")
        return folder
    except Exception as e:
        raise Exception(f"Error retrieving folder with ID '{id}': {str(e)}") from e