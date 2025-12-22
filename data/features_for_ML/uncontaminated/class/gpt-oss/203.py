import pathlib
import tomllib
from typing import Optional


class ProjectInfo:
    _PYPROJECT_PATH = pathlib.Path("pyproject.toml")

    def _load_toml(self) -> Optional[dict]:
        if not self._PYPROJECT_PATH.is_file():
            return None
        try:
            with self._PYPROJECT_PATH.open("rb") as f:
                return tomllib.load(f)
        except Exception:
            return None

    def _get_name_from_pyproject_toml_tool(self) -> str | None:
        data = self._load_toml()
        if not data:
            return None
        tool_section = data.get("tool")
        if not isinstance(tool_section, dict):
            return None
        for subtool in tool_section.values():
            if isinstance(subtool, dict) and "name" in subtool:
                return subtool["name"]
        return None

    def _get_name_from_pyproject_toml_project(self) -> str | None:
        data = self._load_toml()
        if not data:
            return None
        project_section = data.get("project")
        if isinstance(project_section, dict):
            return project_section.get("name")
        return None

    @property
    def name(self) -> str:
        name = self._get_name_from_pyproject_toml_tool()
        if name:
            return name
        name = self._get_name_from_pyproject_toml_project()
        return name or ""