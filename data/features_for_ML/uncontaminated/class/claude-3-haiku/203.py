import toml

class ProjectInfo:
    def __init__(self, pyproject_toml_path: str):
        self._pyproject_toml_path = pyproject_toml_path
        self._pyproject_toml_data = self._load_pyproject_toml()

    def _load_pyproject_toml(self) -> dict:
        try:
            with open(self._pyproject_toml_path, 'r') as file:
                return toml.load(file)
        except (FileNotFoundError, IOError):
            return {}

    def _get_name_from_pyproject_toml_tool(self) -> str | None:
        if 'tool' in self._pyproject_toml_data and 'poetry' in self._pyproject_toml_data['tool']:
            return self._pyproject_toml_data['tool']['poetry'].get('name')
        return None

    def _get_name_from_pyproject_toml_project(self) -> str | None:
        return self._pyproject_toml_data.get('project', {}).get('name')

    @property
    def name(self) -> str:
        name = self._get_name_from_pyproject_toml_tool()
        if name is None:
            name = self._get_name_from_pyproject_toml_project()
        if name is None:
            name = ''
        return name