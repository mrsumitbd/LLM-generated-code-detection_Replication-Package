def get_volumes(self) -> list[tuple[str, str]]:
        """Get Docker volume mappings for home and workspace directories.

        Returns:
            list[tuple[str, str]]: List of (host_path, container_path) tuples
        """
        volumes = []
        if self.home_path and self.home_path.host_path:
            volumes.append(self.home_path.vol())
        if self.workspace_path and self.workspace_path.host_path:
            volumes.append(self.workspace_path.vol())
        return volumes