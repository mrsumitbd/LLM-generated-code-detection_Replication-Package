def copy_folders(
    filtered_folders: list[Folder],
    to_context: Workspace | Folder,
    args: Namespace,
    delete_after_copy: Optional[bool] = False,
) -> int:
    copied_folders = 0
    for folder in filtered_folders:
        new_folder = folder.copy(to_context)
        if delete_after_copy:
            folder.delete()
        copied_folders += 1
    return copied_folders