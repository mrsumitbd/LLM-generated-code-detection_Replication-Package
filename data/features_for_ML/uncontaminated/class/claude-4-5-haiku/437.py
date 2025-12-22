from functools import lru_cache
from typing import Dict, Any

class AppConfig:
    _instance = None
    _config = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        pass

    @classmethod
    @lru_cache()
    def get_instance(cls) -> 'AppConfig':
        return cls()

    def initialize(self, config: Dict[str, Any]) -> None:
        self._config = config.copy()

    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)

    def __getattr__(self, name: str) -> Any:
        if name.startswith('_'):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
        return self._config.get(name)

    def __getitem__(self, key: str) -> Any:
        return self._config[key]

    def __contains__(self, key: str) -> bool:
        return key in self._config