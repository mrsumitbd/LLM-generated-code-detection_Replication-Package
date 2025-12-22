class BackwardCompatibility:
    """Helper functions for maintaining backward compatibility during migration"""

    @staticmethod
    def get_collection_name(project: str, mode: str, version: str = "v4") -> str:
        if version == "v4":
            return f"{project}_{mode}"
        elif version == "v3":
            return f"{project}_{mode}_v3"
        else:
            raise ValueError(f"Unsupported version: {version}")