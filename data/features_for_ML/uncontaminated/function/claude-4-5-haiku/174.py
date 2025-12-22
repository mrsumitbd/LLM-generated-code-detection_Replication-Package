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
            # Create a new folder in the target context with the same name
            new_folder = Folder(
                name=folder.name,
                workspace_id=to_context.workspace_id if isinstance(to_context, Folder) else to_context.id,
                parent_id=to_context.id if isinstance(to_context, Folder) else None,
            )
            
            # Copy folder properties
            if hasattr(folder, 'description'):
                new_folder.description = folder.description
            
            # Save the new folder
            new_folder.save()
            
            # Copy contents if the folder has items
            if hasattr(folder, 'items') and folder.items:
                for item in folder.items:
                    # Copy item to new folder
                    item.copy_to(new_folder)
            
            # Delete original folder if requested
            if delete_after_copy:
                folder.delete()
            
            copied_count += 1
            
            # Log progress if verbose mode is enabled
            if hasattr(args, 'verbose') and args.verbose:
                print(f"Copied folder: {folder.name}")
                
        except Exception as e:
            # Log error if verbose mode is enabled
            if hasattr(args, 'verbose') and args.verbose:
                print(f"Error copying folder {folder.name}: {str(e)}")
            continue
    
    return copied_count