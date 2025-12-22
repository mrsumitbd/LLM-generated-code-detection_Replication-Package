from typing import Namespace, Optional
from dataclasses import dataclass

@dataclass
class Folder:
    name: str
    path: str

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
    copied_count = 0
    for folder in filtered_folders:
        try:
            to_context.create_folder(folder.name, folder.path)
            copied_count += 1
            if delete_after_copy:
                folder.delete()
        except Exception as e:
            print(f"Error copying folder '{folder.name}': {e}")
    return copied_count