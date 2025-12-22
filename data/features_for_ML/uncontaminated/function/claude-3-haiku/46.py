import os
import json

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
    if config_path:
        return _apply_config_from_path(config_path)

    if search_paths and file_names:
        for search_path in search_paths:
            for file_name in file_names:
                config_path = os.path.join(search_path, file_name)
                if os.path.exists(config_path):
                    return _apply_config_from_path(config_path)

    return False

def _apply_config_from_path(config_path: str) -> bool:
    try:
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        # Apply the configuration
        # ...
        return True
    except (IOError, ValueError):
        return False