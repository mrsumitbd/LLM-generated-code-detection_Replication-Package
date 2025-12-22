from argparse import Namespace
from typing import Optional
from fabric_cli.core.hiearchy.fab_folder import Folder
from fabric_cli.core.hiearchy.fab_hiearchy import Folder, Item, Workspace

def copy_folders(
    filtered_folders: list[Folder],
    to_context: Workspace | Folder,
    args: Namespace,
    delete_after_copy: Optional[bool] = False,
) -> int:
    """
    Copy a list of folders to the specified context (Workspace or Folder).
    If delete_after_copy is True, the original folders will be deleted after copying.
    """
    successful_copies = 0

    for folder in filtered_folders:
        successful_copies += copy_folder(
            from_folder=folder,
            to_context=to_context,
            args=args,
            delete_after_copy=delete_after_copy,
        )

    return successful_copies