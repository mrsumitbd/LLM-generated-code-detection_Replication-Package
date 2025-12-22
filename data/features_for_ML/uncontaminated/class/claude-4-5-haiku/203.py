class ProjectInfo:
    def __init__(self, pyproject_path: str | None = None):
        self.pyproject_path = pyproject_path
        self._pyproject_data = None

    def _load_pyproject(self) -> dict:
        if self._pyproject_data is not None:
            return self._pyproject_data
        
        if self.pyproject_path is None:
            self._pyproject_data = {}
            return self._pyproject_data
        
        try:
            import tomllib
        except ImportError:
            import tomli as tomllib
        
        try:
            with open(self.pyproject_path, 'rb') as f:
                self._pyproject_data = tomllib.load(f)
        except (FileNotFoundError, Exception):
            self._pyproject_data = {}
        
        return self._pyproject_data

    def _get_name_from_pyproject_toml_tool(self) -> str | None:
        pyproject = self._load_pyproject()
        
        if 'tool' not in pyproject:
            return None
        
        tool = pyproject['tool']
        
        if 'poetry' in tool and 'name' in tool['poetry']:
            return tool['poetry']['name']
        
        if 'setuptools' in tool and 'name' in tool['setuptools']:
            return tool['setuptools']['name']
        
        return None

    def _get_name_from_pyproject_toml_project(self) -> str | None:
        pyproject = self._load_pyproject()
        
        if 'project' not in pyproject:
            return None
        
        project = pyproject['project']
        
        if 'name' in project:
            return project['name']
        
        return None

    @property
    def name(self) -> str:
        name = self._get_name_from_pyproject_toml_project()
        if name is not None:
            return name
        
        name = self._get_name_from_pyproject_toml_tool()
        if name is not None:
            return name
        
        return "unknown"