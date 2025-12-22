def get_volumes(self) -> list[tuple[str, str]]:
    """Get Docker volume mappings for home and workspace directories.

    Returns:
        list[tuple[str, str]]: List of (host_path, container_path) tuples
    """
    home_dir = os.path.expanduser("~")
    workspace_dir = os.path.join(home_dir, "workspace")

    return [
        (home_dir, "/home/user"),
        (workspace_dir, "/workspace")
    ]