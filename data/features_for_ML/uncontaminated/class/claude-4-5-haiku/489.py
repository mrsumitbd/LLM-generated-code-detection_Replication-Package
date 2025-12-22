class BackwardCompatibility:
    """Helper functions for maintaining backward compatibility during migration"""

    @staticmethod
    def get_collection_name(project: str, mode: str, version: str = "v4") -> str:
        """
        Generate a collection name based on project, mode, and version.
        
        Args:
            project: The project name
            mode: The mode (e.g., 'read', 'write', 'sync')
            version: The version string (default: "v4")
        
        Returns:
            A formatted collection name string
        """
        if version == "v4":
            return f"{project}_{mode}"
        else:
            return f"{project}_{mode}_{version}"