from __future__ import annotations

import sys
from typing import Optional

from argparse import Namespace


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

    # Helper to perform the copy operation
    def _copy_one(folder: Folder) -> Folder | None:
        # If the folder itself knows how to copy to a context
        if hasattr(folder, "copy"):
            try:
                return folder.copy(to_context)
            except Exception as exc:
                print(
                    f"Error copying folder '{folder.name}' via folder.copy: {exc}",
                    file=sys.stderr,
                )
                return None

        # If the target context knows how to copy a folder into it
        if hasattr(to_context, "copy_folder"):
            try:
                return to_context.copy_folder(folder)
            except Exception as exc:
                print(
                    f"Error copying folder '{folder.name}' via to_context.copy_folder: {exc}",
                    file=sys.stderr,
                )
                return None

        # Fallback: try a generic copy method on the context
        if hasattr(to_context, "copy"):
            try:
                return to_context.copy(folder)
            except Exception as exc:
                print(
                    f"Error copying folder '{folder.name}' via to_context.copy: {exc}",
                    file=sys.stderr,
                )
                return None

        # No known copy mechanism
        print(
            f"No copy method found for folder '{folder.name}' to context '{to_context}'.",
            file=sys.stderr,
        )
        return None

    for folder in filtered_folders:
        if getattr(args, "dry_run", False):
            print(
                f"[DRY-RUN] Would copy folder '{folder.name}' to '{to_context}'."
            )
            continue

        new_folder = _copy_one(folder)
        if new_folder is None:
            continue

        if delete_after_copy:
            try:
                if hasattr(folder, "delete"):
                    folder.delete()
                else:
                    print(
                        f"Folder '{folder.name}' has no delete method; skipping deletion.",
                        file=sys.stderr,
                    )
            except Exception as exc:
                print(
                    f"Error deleting original folder '{folder.name}': {exc}",
                    file=sys.stderr,
                )

        if getattr(args, "verbose", False):
            print(
                f"Copied folder '{folder.name}' to '{to_context}'. New folder ID: {getattr(new_folder, 'id', 'unknown')}"
            )

        copied_count += 1

    return copied_count