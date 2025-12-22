from .manager import config

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
    try:
        # Find config file
        file_path = find_config_file(config_path, search_paths, file_names)
        if not file_path:
            logger.debug("No configuration file found")
            return False

        # Load config file
        logger.info(f"Loading configuration from {file_path}")
        config_data = load_config_file(file_path)

        # Load custom transports if configured
        load_custom_transports(config_data)

        # Apply configuration
        config.update(config_data)
        return True
    except Exception as e:
        logger.error(f"Error loading configuration file: {str(e)}")
        return False