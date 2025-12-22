from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import BaseSettings, Field, validator


class Config(BaseSettings):
    """
    Pydantic configuration for application settings.

    This class loads configuration from environment variables, a .env file,
    and allows overriding defaults via keyword arguments.
    """

    # ------------------------------------------------------------------
    # Core settings
    # ------------------------------------------------------------------
    debug: bool = Field(
        default=False,
        description="Enable debug mode for the application.",
    )
    host: str = Field(
        default="127.0.0.1",
        description="The host address the server will bind to.",
    )
    port: int = Field(
        default=8000,
        description="The port number the server will listen on.",
    )
    database_url: str = Field(
        default="sqlite:///./test.db",
        description="Database connection URL.",
    )
    secret_key: str = Field(
        default="changeme",
        description="Secret key used for cryptographic operations.",
    )
    allowed_hosts: list[str] = Field(
        default_factory=lambda: ["*"],
        description="List of hosts that are allowed to connect.",
    )

    # ------------------------------------------------------------------
    # Environment file handling
    # ------------------------------------------------------------------
    env_file: str = ".env"
    env_file_encoding: str = "utf-8"

    # ------------------------------------------------------------------
    # Pydantic configuration
    # ------------------------------------------------------------------
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        arbitrary_types_allowed = True
        orm_mode = True
        use_enum_values = True
        validate_assignment = True
        allow_population_by_field_name = True

    # ------------------------------------------------------------------
    # Validators
    # ------------------------------------------------------------------
    @validator("port")
    def port_must_be_valid(cls, v: int) -> int:
        if not (0 < v < 65536):
            raise ValueError("port must be between 1 and 65535")
        return v

    @validator("allowed_hosts", pre=True)
    def split_allowed_hosts(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            return [host.strip() for host in v.split(",") if host.strip()]
        if isinstance(v, list):
            return v
        raise ValueError("allowed_hosts must be a list or comma-separated string")

    # ------------------------------------------------------------------
    # Utility methods
    # ------------------------------------------------------------------
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Config":
        """
        Create a Config instance from a dictionary.
        """
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        """
        Return the configuration as a dictionary.
        """
        return self.dict()

    @classmethod
    def load_from_file(cls, path: Path | str) -> "Config":
        """
        Load configuration from a JSON or YAML file.
        """
        import json
        import yaml

        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path}")

        if path.suffix in {".json"}:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        elif path.suffix in {".yaml", ".yml"}:
            with path.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        else:
            raise ValueError("Unsupported configuration file format")

        return cls.from_dict(data)

    @classmethod
    def from_env(cls, env_prefix: str = "") -> "Config":
        """
        Load configuration from environment variables with an optional prefix.
        """
        env_vars = {
            key[len(env_prefix) :]: value
            for key, value in os.environ.items()
            if key.startswith(env_prefix)
        }
        return cls(**env_vars)

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        fields = ", ".join(f"{k}={v!r}" for k, v in self.dict().items())
        return f"{self.__class__.__name__}({fields})"