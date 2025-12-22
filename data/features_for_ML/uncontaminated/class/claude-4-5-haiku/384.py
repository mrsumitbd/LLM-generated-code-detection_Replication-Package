from pathlib import Path
import yaml
import os
from typing import Any, Dict

class ProductionConfig:
    def __init__(self, config_dict: Dict[str, Any] = None):
        if config_dict is None:
            config_dict = {}
        self.config = config_dict
        self.database_url = config_dict.get('database_url', '')
        self.debug = config_dict.get('debug', False)
        self.secret_key = config_dict.get('secret_key', '')
        self.log_level = config_dict.get('log_level', 'INFO')
        self.workers = config_dict.get('workers', 4)
        self.host = config_dict.get('host', '0.0.0.0')
        self.port = config_dict.get('port', 8000)

    @classmethod
    def _from_yaml(cls, path: Path) -> "ProductionConfig":
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
        
        with open(path, 'r') as f:
            config_dict = yaml.safe_load(f)
        
        if config_dict is None:
            config_dict = {}
        
        return cls(config_dict)

    @classmethod
    def _apply_env_overrides(cls, cfg: "ProductionConfig") -> "ProductionConfig":
        env_mappings = {
            'DATABASE_URL': 'database_url',
            'DEBUG': 'debug',
            'SECRET_KEY': 'secret_key',
            'LOG_LEVEL': 'log_level',
            'WORKERS': 'workers',
            'HOST': 'host',
            'PORT': 'port',
        }
        
        for env_var, config_key in env_mappings.items():
            env_value = os.getenv(env_var)
            if env_value is not None:
                if config_key == 'debug':
                    setattr(cfg, config_key, env_value.lower() in ('true', '1', 'yes'))
                elif config_key in ('workers', 'port'):
                    setattr(cfg, config_key, int(env_value))
                else:
                    setattr(cfg, config_key, env_value)
                cfg.config[config_key] = getattr(cfg, config_key)
        
        return cfg

    @classmethod
    def load(cls, yaml_path: str = "config.yaml") -> "ProductionConfig":
        path = Path(yaml_path)
        cfg = cls._from_yaml(path)
        cfg = cls._apply_env_overrides(cfg)
        cfg.validate()
        return cfg

    def validate(self) -> None:
        if not self.database_url:
            raise ValueError("database_url is required")
        
        if not self.secret_key:
            raise ValueError("secret_key is required")
        
        if self.port < 1 or self.port > 65535:
            raise ValueError(f"port must be between 1 and 65535, got {self.port}")
        
        if self.workers < 1:
            raise ValueError(f"workers must be at least 1, got {self.workers}")
        
        valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if self.log_level.upper() not in valid_log_levels:
            raise ValueError(f"log_level must be one of {valid_log_levels}, got {self.log_level}")