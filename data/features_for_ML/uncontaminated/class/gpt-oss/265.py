from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session


@dataclass
class Config:
    """SQLModel configuration."""

    # Connection URL – defaults to a local SQLite database
    database_url: str = field(
        default_factory=lambda: os.getenv("DATABASE_URL", "sqlite:///./test.db")
    )
    # Echo SQL statements to the console
    echo: bool = False
    # Connection pool size
    pool_size: int = 5
    # Maximum overflow connections
    max_overflow: int = 10
    # Use SQLAlchemy 2.0 style
    future: bool = True
    # Enable pool pre‑ping
    pool_pre_ping: bool = True

    def engine(self) -> Engine:
        """Create a SQLAlchemy engine based on the configuration."""
        return create_engine(
            self.database_url,
            echo=self.echo,
            pool_size=self.pool_size,
            max_overflow=self.max_overflow,
            future=self.future,
            pool_pre_ping=self.pool_pre_ping,
        )

    def sessionmaker(self) -> sessionmaker:
        """Return a sessionmaker bound to the configured engine."""
        return sessionmaker(bind=self.engine(), autoflush=False, autocommit=False)

    @classmethod
    def from_env(cls, env_prefix: str = "SQLMODEL_") -> "Config":
        """
        Build a Config instance from environment variables.

        Environment variable names are derived from the field names
        prefixed with `env_prefix`. For example, `SQLMODEL_DATABASE_URL`.
        """
        kwargs: Dict[str, Any] = {}
        for field_name, field_def in cls.__dataclass_fields__.items():
            env_var = f"{env_prefix}{field_name.upper()}"
            if env_var in os.environ:
                raw_value = os.environ[env_var]
                field_type = field_def.type
                # Convert string env values to the correct type
                if field_type is bool:
                    raw_value = raw_value.lower() in ("1", "true", "yes", "on")
                elif field_type is int:
                    raw_value = int(raw_value)
                kwargs[field_name] = raw_value
        return cls(**kwargs)

    def __repr__(self) -> str:
        return (
            f"<Config database_url={self.database_url!r} echo={self.echo} "
            f"pool_size={self.pool_size} max_overflow={self.max_overflow}>"
        )