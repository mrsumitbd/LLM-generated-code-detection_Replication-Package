from pathlib import Path

class ProductionConfig:

    @classmethod
    def _from_yaml(cls, path: Path) -> "ProductionConfig":
        # Implementation for loading configuration from YAML file
        pass

    @classmethod
    def _apply_env_overrides(cls, cfg: "ProductionConfig") -> "ProductionConfig":
        # Implementation for applying environment overrides to configuration
        pass

    @classmethod
    def load(cls, yaml_path: str = "config.yaml") -> "ProductionConfig":
        config = cls._from_yaml(Path(yaml_path))
        config = cls._apply_env_overrides(config)
        return config

    def validate(self) -> None:
        # Implementation for validating the configuration
        pass