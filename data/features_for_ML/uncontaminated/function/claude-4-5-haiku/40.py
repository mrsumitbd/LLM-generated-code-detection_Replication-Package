def get_volumes(self) -> list[tuple[str, str]]:
    """Get Docker volume mappings for home and workspace directories.

    Returns:
        list[tuple[str, str]]: List of (host_path, container_path) tuples
    """
    volumes = []
    
    if hasattr(self, 'home_dir') and self.home_dir:
        volumes.append((self.home_dir, '/root'))
    
    if hasattr(self, 'workspace_dir') and self.workspace_dir:
        volumes.append((self.workspace_dir, '/workspace'))
    
    return volumes