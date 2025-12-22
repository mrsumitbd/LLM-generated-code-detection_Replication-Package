import os
from pathlib import Path
from typing import Any, Dict

import yaml


class ProductionConfig:
    """
    Simple configuration loader that:
    * Loads a YAML file into a dictionary.
    * Applies environment variable overrides for top‑level keys.
    * Provides a basic validation step.
    """

    def __init__(self, data: Dict[str, Any]):
        # Store the raw configuration dictionary
        self._data = data

    # ------------------------------------------------------------------
    # Class helpers
    # ------------------------------------------------------------------
    @classmethod
    def _from_yaml(cls, path: Path) -> "ProductionConfig":
        """
        Load a YAML file and return a ProductionConfig instance.
        """
        if not path.is_file():
            raise FileNotFoundError(f"Configuration file not found: {path}")
        with path.open("r", encoding="utf-8") as f:
            raw = yaml.safe_load(f) or {}
        if not isinstance(raw, dict):
            raise ValueError("YAML root must be a mapping")
        return cls(raw)

    @classmethod
    def _apply_env_overrides(cls, cfg: "ProductionConfig") -> "ProductionConfig":
        """
        Override top‑level configuration values with environment variables.
        Environment variable names are the uppercase form of the key.
        """
        for key in list(cfg._data.keys()):
            env_key = key.upper()
            if env_key in os.environ:
                # Try to interpret the env value as JSON; fall back to string
                try:
                    val = yaml.safe_load(os.environ[env_key])
                except Exception:
                    val = os.environ[env_key]
                cfg._data[key] = val
        return cfg

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    @classmethod
    def load(cls, yaml_path: str = "config.yaml") -> "ProductionConfig":
        """
        Load configuration from a YAML file, apply environment overrides,
        and return a validated ProductionConfig instance.
        """
        cfg = cls._from_yaml(Path(yaml_path))
        cfg = cls._apply_env_overrides(cfg)
        cfg.validate()
        return cfg

    def validate(self) -> None:
        """
        Basic validation: ensure required top‑level keys exist.
        Override this method for more complex validation logic.
        """
        required_keys = {"database", "api_key"}
        missing = required_keys - self._data.keys()
        if missing:
            raise ValueError(f"Missing required configuration keys: {missing}")

    # ------------------------------------------------------------------
    # Convenience accessors
    # ------------------------------------------------------------------
    def __getattr__(self, name: str) -> Any:
        """
        Allow attribute access to configuration keys.
        """
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"{self.__class__.__name__!r} has no attribute {name!r}")

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self._data!r}>"