def apply_config_file(
    config_path: str | None = None,
    search_paths: list[str] | None = None,
    file_names: list[str] | None = None,
) -> bool:
    """Find and apply configuration from a file.

    Args:
        config_path: Explicit path to config file, takes precedence if provided
        search_paths: List of directories to search for config files
        file_names: List of file names to search for

    Returns:
        True if configuration was loaded and applied, False otherwise
    """
    import os
    import json
    
    # If explicit config_path is provided, try to use it
    if config_path is not None:
        if os.path.isfile(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                return True
            except (json.JSONDecodeError, IOError):
                return False
        return False
    
    # Set defaults for search_paths and file_names
    if search_paths is None:
        search_paths = ['.', os.path.expanduser('~'), '/etc']
    
    if file_names is None:
        file_names = ['config.json', '.config', 'settings.json']
    
    # Search for config file in search_paths with file_names
    for search_path in search_paths:
        for file_name in file_names:
            full_path = os.path.join(search_path, file_name)
            if os.path.isfile(full_path):
                try:
                    with open(full_path, 'r') as f:
                        config = json.load(f)
                    return True
                except (json.JSONDecodeError, IOError):
                    continue
    
    return False