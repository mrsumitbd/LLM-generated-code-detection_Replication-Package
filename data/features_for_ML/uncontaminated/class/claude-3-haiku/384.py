import os
from pathlib import Path
import yaml

class ProductionConfig:

    def __init__(self, data: dict):
        self.data = data

    @classmethod
    def _from_yaml(cls, path: Path) -> "ProductionConfig":
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        return cls(data)

    @classmethod
    def _apply_env_overrides(cls, cfg: "ProductionConfig") -> "ProductionConfig":
        for key, value in os.environ.items():
            if key.startswith("CONFIG_"):
                cfg.data[key[7:].lower()] = value
        return cfg

    @classmethod
    def load(cls, yaml_path: str = "config.yaml") -> "ProductionConfig":
        path = Path(yaml_path)
        cfg = cls._from_yaml(path)
        cfg = cls._apply_env_overrides(cfg)
        return cfg

    def validate(self) -> None:
        # Implement validation logic here
        pass