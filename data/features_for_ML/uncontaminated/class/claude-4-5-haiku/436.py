class CodemodManager:
    """Manages codemod operations in the local filesystem."""

    @staticmethod
    def get_valid_name(name: str) -> str:
        """Convert a name to a valid codemod name format."""
        return name.strip().lower().replace(" ", "_").replace("-", "_")

    @classmethod
    def get_codemod(cls, name: str, start_path: Path | None = None) -> DecoratedFunction:
        """Get a codemod by name, raising an error if not found."""
        valid_name = cls.get_valid_name(name)
        codemod = cls.get(valid_name, start_path)
        if codemod is None:
            raise ValueError(f"Codemod '{name}' not found")
        return codemod

    @classmethod
    def list(cls, start_path: Path | None = None) -> builtins.list[DecoratedFunction]:
        """List all available codemods."""
        return cls.get_decorated(start_path)

    @classmethod
    def get(cls, name: str, start_path: Path | None = None) -> DecoratedFunction | None:
        """Get a codemod by name, returning None if not found."""
        valid_name = cls.get_valid_name(name)
        decorated_list = cls.get_decorated(start_path)
        for codemod in decorated_list:
            if cls.get_valid_name(codemod.name) == valid_name:
                return codemod
        return None

    @classmethod
    def exists(cls, name: str, start_path: Path | None = None) -> bool:
        """Check if a codemod exists."""
        return cls.get(name, start_path) is not None

    @classmethod
    def get_decorated(cls, start_path: Path | None = None) -> builtins.list[DecoratedFunction]:
        """Get all decorated codemod functions from the filesystem."""
        if start_path is None:
            start_path = Path.cwd()
        
        decorated_functions = []
        
        if not start_path.exists():
            return decorated_functions
        
        for item in start_path.rglob("*.py"):
            if item.is_file():
                try:
                    spec = importlib.util.spec_from_file_location(
                        item.stem, item
                    )
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        
                        for attr_name in dir(module):
                            attr = getattr(module, attr_name)
                            if isinstance(attr, DecoratedFunction):
                                decorated_functions.append(attr)
                except Exception:
                    pass
        
        return decorated_functions