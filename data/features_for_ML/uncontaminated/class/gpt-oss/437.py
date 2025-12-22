from functools import lru_cache
from typing import Any, Dict


class AppConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppConfig, cls).__new__(cls)
            cls._instance._config = {}
        return cls._instance

    def __init__(self):
        # __init__ may be called multiple times due to singleton pattern;
        # we only need to ensure the config dict exists.
        if not hasattr(self, "_config"):
            self._config = {}

    @classmethod
    @lru_cache()
    def get_instance(cls) -> "AppConfig":
        return cls()

    def initialize(self, config: Dict[str, Any]) -> None:
        """Load configuration values."""
        self._config = dict(config)

    def get(self, key: str, default: Any = None) -> Any:
        """Return the value for *key* or *default* if not present."""
        return self._config.get(key, default)

    def __getattr__(self, name: str) -> Any:
        """Allow attribute access to configuration keys."""
        if name in self._config:
            return self._config[name]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __getitem__(self, key: str) -> Any:
        """Allow dict-like access to configuration values."""
        return self.get(key)

    def __contains__(self, key: str) -> bool:
        """Check if a configuration key exists."""
        return key in self._config