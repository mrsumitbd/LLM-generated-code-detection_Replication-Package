class BackwardCompatibility:
    """Helper functions for maintaining backward compatibility during migration"""

    @staticmethod
    def get_collection_name(project: str, mode: str, version: str = "v4") -> str:
        """
        Construct a collection name based on the project, mode, and version.

        Parameters
        ----------
        project : str
            The project identifier.
        mode : str
            The mode identifier (e.g., 'train', 'test', etc.).
        version : str, optional
            The version string. Defaults to "v4".

        Returns
        -------
        str
            The constructed collection name.
        """
        # Normalise inputs: strip whitespace, replace spaces with underscores, lower‑case
        proj = project.strip().replace(" ", "_")
        mod = mode.strip().replace(" ", "_")

        # For the legacy v4 format we omit the version suffix
        if version == "v4":
            return f"{proj}_{mod}"
        # For newer versions we include the version suffix
        return f"{proj}_{mod}_{version}"