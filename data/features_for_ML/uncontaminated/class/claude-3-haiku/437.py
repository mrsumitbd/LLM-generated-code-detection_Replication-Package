from functools import lru_cache
from typing import Dict, Any

class AppConfig:

    def __new__(cls):
        instance = super().__new__(cls)
        return instance

    def __init__(self):
        self._config = {}

    @classmethod
    @lru_cache()
    def get_instance(cls) -> 'AppConfig':
        return cls()

    def initialize(self, config: Dict[str, Any]) -> None:
        self._config = config

    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)

    def __getattr__(self, name: str) -> Any:
        return self._config.get(name, None)

    def __getitem__(self, key: str) -> Any:
        return self._config[key]

    def __contains__(self, key: str) -> bool:
        return key in self._config