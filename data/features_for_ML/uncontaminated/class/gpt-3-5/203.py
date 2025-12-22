class ProjectInfo:

    def _get_name_from_pyproject_toml_tool(self) -> str | None:
        # Implementation to get project name from pyproject.toml tool section
        return "Project Name from tool section"

    def _get_name_from_pyproject_toml_project(self) -> str | None:
        # Implementation to get project name from pyproject.toml project section
        return "Project Name from project section"

    @property
    def name(self) -> str:
        name_from_tool = self._get_name_from_pyproject_toml_tool()
        name_from_project = self._get_name_from_pyproject_toml_project()
        
        if name_from_tool:
            return name_from_tool
        elif name_from_project:
            return name_from_project
        else:
            return "Unknown Project Name"