def _enumerate_files(
        paths: list[str],
        valid_file_extension: str,
        exclude_pattern: Optional[str] = None,
        recursive: bool = False
    ) -> List[str]:
    r"""Enumerate files in a folder based on include and exclude patterns.

    Args:
        paths: paths to the folders to traverse, these will be glob patterns.
        exclude_pattern: Regex pattern to exclude files (e.g., r"\.tmp$", r"temp.*")
        recursive: Whether to traverse subdirectories recursively

    Returns:
        List of Path objects for matching files
    """
    import glob
    import re
    from pathlib import Path
    
    matching_files = []
    exclude_regex = re.compile(exclude_pattern) if exclude_pattern else None
    
    for path_pattern in paths:
        # Expand glob patterns
        expanded_paths = glob.glob(path_pattern, recursive=recursive)
        
        for expanded_path in expanded_paths:
            path_obj = Path(expanded_path)
            
            # If it's a file, check it directly
            if path_obj.is_file():
                # Check file extension
                if path_obj.suffix == valid_file_extension or valid_file_extension == "*":
                    # Check exclude pattern
                    if exclude_regex is None or not exclude_regex.search(str(path_obj)):
                        matching_files.append(str(path_obj))
            
            # If it's a directory, traverse it
            elif path_obj.is_dir():
                if recursive:
                    # Recursive search
                    pattern = f"**/*{valid_file_extension}" if valid_file_extension != "*" else "**/*"
                    for file_path in path_obj.glob(pattern):
                        if file_path.is_file():
                            if exclude_regex is None or not exclude_regex.search(str(file_path)):
                                matching_files.append(str(file_path))
                else:
                    # Non-recursive search
                    pattern = f"*{valid_file_extension}" if valid_file_extension != "*" else "*"
                    for file_path in path_obj.glob(pattern):
                        if file_path.is_file():
                            if exclude_regex is None or not exclude_regex.search(str(file_path)):
                                matching_files.append(str(file_path))
    
    return matching_files