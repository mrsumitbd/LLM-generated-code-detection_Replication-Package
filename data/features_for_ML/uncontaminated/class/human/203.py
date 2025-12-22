import re
from pathlib import Path
import tomllib
from typing import Any

class ProjectInfo:
    root_dir: Path

    pyproject_toml: str = NOT_FOUND
    setup_py: str = NOT_FOUND
    setup_cfg: str = NOT_FOUND
    readme: str = NOT_FOUND

    def _get_name_from_pyproject_toml_tool(self) -> str | None:
        pyproject_dict: dict[str, Any] = tomllib.loads(self.pyproject_toml)
        try:
            return pyproject_dict["tool"]["poetry"]["name"].lower()
        except KeyError:
            return None

    def _get_name_from_pyproject_toml_project(self) -> str | None:
        pyproject_dict: dict[str, Any] = tomllib.loads(self.pyproject_toml)
        try:
            return pyproject_dict["project"]["name"].lower()
        except KeyError:
            return None

    @property
    def name(self) -> str:
        if self.pyproject_toml != NOT_FOUND:
            if result := self._get_name_from_pyproject_toml_tool():
                return result

            if result := self._get_name_from_pyproject_toml_project():
                return result

        if self.setup_py != NOT_FOUND:
            pattern = r"name ?= ?(\"|'| )?(?P<name>[\w\-_]+)(\"|'| )?"
            match = re.search(pattern, self.setup_py)
            if match:
                return match.group("name").lower()

        if self.setup_cfg != NOT_FOUND:
            pattern = r"name ?= ?(\"|'| )?(?P<name>[\w\-_]+)(\"|'| )?"
            match = re.search(pattern, self.setup_cfg)
            if match:
                return match.group("name").lower()

        raise Exception("Project name not found. This is critical problem.")