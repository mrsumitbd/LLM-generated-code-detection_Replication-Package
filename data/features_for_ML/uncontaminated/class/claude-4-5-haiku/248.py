class LastUsedParams:
    """Manages last used parameters persistence (moved from last_used.py)."""

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        if config_dir is None:
            config_dir = Path.home() / ".config" / "app"
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = self.config_dir / "last_used_params.json"

    def save(self, settings: "Settings") -> None:
        data = {}
        if hasattr(settings, '__dict__'):
            for key, value in settings.__dict__.items():
                if isinstance(value, (str, int, float, bool, list, dict, type(None))):
                    data[key] = value
                elif isinstance(value, Path):
                    data[key] = str(value)
                else:
                    try:
                        data[key] = str(value)
                    except Exception:
                        pass
        
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)

    def load(self) -> Dict[str, Any]:
        if not self.file_path.exists():
            return {}
        
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def clear(self) -> None:
        if self.file_path.exists():
            self.file_path.unlink()

    def exists(self) -> bool:
        return self.file_path.exists()