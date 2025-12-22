from typing import Iterable

def get_folder(workspace: "Workspace", id: str) -> "Folder":
    """
    Retrieve a Folder instance from a Workspace by its identifier.

    Parameters
    ----------
    workspace : Workspace
        The workspace object that contains folders.
    id : str
        The unique identifier of the folder to retrieve.

    Returns
    -------
    Folder
        The folder instance with the matching identifier.

    Raises
    ------
    KeyError
        If no folder with the given identifier is found in the workspace.
    """
    # Try a direct method if the workspace provides one
    try:
        return workspace.get_folder(id)
    except AttributeError:
        pass

    # Fallback: iterate over a collection of folders
    folders: Iterable = getattr(workspace, "folders", [])
    for folder in folders:
        # Use getattr to avoid AttributeError if the folder object
        # does not expose an `id` attribute directly.
        if getattr(folder, "id", None) == id:
            return folder

    # If we reach this point, the folder was not found
    raise KeyError(f"Folder with id '{id}' not found in workspace '{workspace}'.")