from __future__ import annotations

import threading
from dataclasses import dataclass
from typing import Optional

from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    text,
)
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker


# --------------------------------------------------------------------------- #
# Configuration dataclass
# --------------------------------------------------------------------------- #
@dataclass
class DatabaseConfig:
    """Simple configuration holder for the database engine."""

    url: str = "sqlite:///./benchmark.db"
    echo: bool = False
    pool_size: int = 5
    max_overflow: int = 10


# --------------------------------------------------------------------------- #
# DatabaseEngine singleton
# --------------------------------------------------------------------------- #
class DatabaseEngine:
    """SQLAlchemy engine service (singleton)."""

    _instance: Optional["DatabaseEngine"] = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls, config: DatabaseConfig = None):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config: DatabaseConfig = None):
        # Avoid re‑initialisation on subsequent calls
        if hasattr(self, "_engine"):
            return

        if config is None:
            config = DatabaseConfig()

        self._config = config
        self._engine: Engine = create_engine(
            config.url,
            echo=config.echo,
            pool_size=config.pool_size,
            max_overflow=config.max_overflow,
        )
        self._SessionLocal = sessionmaker(bind=self._engine, autoflush=False, autocommit=False)

        # Ensure the database schema exists and seed data
        self._ensure_schema()
        self._seed_benchmark_data()

    # ----------------------------------------------------------------------- #
    # Public API
    # ----------------------------------------------------------------------- #
    @property
    def engine(self) -> Engine:
        """Return the underlying SQLAlchemy engine."""
        return self._engine

    @property
    def session(self):
        """Return a new session instance."""
        return self._SessionLocal()

    # ----------------------------------------------------------------------- #
    # Internal helpers
    # ----------------------------------------------------------------------- #
    def _ensure_schema(self):
        """Create the benchmark table if it does not exist."""
        metadata = MetaData()
        self._benchmark_table = Table(
            "benchmark",
            metadata,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("name", String(50), nullable=False),
            Column("value", Integer, nullable=False),
        )
        metadata.create_all(self._engine)

    def _seed_benchmark_data(self):
        """Insert sample benchmark data if the table is empty."""
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM benchmark"))
            count = result.scalar_one()
            if count > 0:
                return  # already seeded

            sample_data = [
                {"name": "load_test", "value": 120},
                {"name": "query_perf", "value": 85},
                {"name": "write_speed", "value": 200},
            ]
            conn.execute(self._benchmark_table.insert(), sample_data)
            conn.commit()