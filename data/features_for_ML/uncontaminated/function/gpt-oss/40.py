def get_volumes(self) -> list[tuple[str, str]]:
    """Get Docker volume mappings for home and workspace directories.

    Returns:
        list[tuple[str, str]]: List of (host_path, container_path) tuples
    """
    volumes: list[tuple[str, str]] = []

    # Home directory mapping
    host_home = getattr(self, "home_dir", None)
    container_home = getattr(self, "container_home_dir", "/home/user")
    if host_home:
        volumes.append((host_home, container_home))

    # Workspace directory mapping
    host_ws = getattr(self, "workspace_dir", None)
    container_ws = getattr(self, "container_workspace_dir", "/workspace")
    if host_ws:
        volumes.append((host_ws, container_ws))

    return volumes