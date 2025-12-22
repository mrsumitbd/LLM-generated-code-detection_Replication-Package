def _enumerate_files(
        paths: list[str],
        valid_file_extension: str,
        exclude_pattern: Optional[str] = None,
        recursive: bool = False
    ) -> List[str]:
    
    import os
    import fnmatch
    
    def _list_files(directory, extension, exclude_pattern):
        files = []
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                if fnmatch.fnmatch(filename, f"*.{extension}") and (exclude_pattern is None or not re.search(exclude_pattern, filename)):
                    files.append(os.path.join(root, filename))
        return files
    
    import re
    import fnmatch
    
    matching_files = []
    for path in paths:
        if os.path.isdir(path):
            if recursive:
                matching_files.extend(_list_files(path, valid_file_extension, exclude_pattern))
            else:
                for filename in os.listdir(path):
                    if fnmatch.fnmatch(filename, f"*.{valid_file_extension}") and (exclude_pattern is None or not re.search(exclude_pattern, filename)):
                        matching_files.append(os.path.join(path, filename))
    
    return matching_files