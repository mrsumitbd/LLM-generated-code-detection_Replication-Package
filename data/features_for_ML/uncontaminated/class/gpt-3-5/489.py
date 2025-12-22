class BackwardCompatibility:
    """Helper functions for maintaining backward compatibility during migration"""

    @staticmethod
    def get_collection_name(project: str, mode: str, version: str = "v4") -> str:
        return f"{project}_{mode}_{version}"