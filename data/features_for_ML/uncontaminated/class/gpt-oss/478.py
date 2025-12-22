from __future__ import annotations

import sqlite3
import threading
from dataclasses import dataclass
from typing import Any, Dict, Optional

# --------------------------------------------------------------------------- #
# Minimal stubs for the types used in the skeleton
# --------------------------------------------------------------------------- #

class Depends:
    """A very small stub for dependency injection placeholders."""
    def __init__(self, name: str):
        self.name = name

@dataclass
class DatabaseConfig:
    """Simple configuration holder for the database connection."""
    dsn: str = ":memory:"  # default to an in‑memory SQLite database

# --------------------------------------------------------------------------- #
# DatabaseService implementation
# --------------------------------------------------------------------------- #

class DatabaseService:
    """Database service (singleton scope)"""

    _instance: Optional["DatabaseService"] = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        """Ensure only one instance is created (singleton)."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config: DatabaseConfig = Depends("db_config")):
        # Avoid re‑initialisation on subsequent calls
        if getattr(self, "_initialized", False):
            return

        # Resolve the dependency if a Depends instance is passed
        if isinstance(config, Depends):
            # In a real DI framework this would be resolved automatically.
            # Here we simply use the default configuration.
            config = DatabaseConfig()

        self.config: DatabaseConfig = config
        self._connection: sqlite3.Connection = sqlite3.connect(
            self.config.dsn, check_same_thread=False
        )
        self._cursor: sqlite3.Cursor = self._connection.cursor()
        self._query_count: int = 0

        self._initialized = True

    def execute_query(self, query: str) -> Dict[str, Any]:
        """
        Execute a SQL query and return the result as a dictionary.
        The dictionary contains:
            - 'rows': a list of row dictionaries (column name → value)
            - 'rowcount': number of rows affected
        """
        self._cursor.execute(query)
        self._connection.commit()
        self._query_count += 1

        # Try to fetch results if the query returns rows
        try:
            rows = self._cursor.fetchall()
            columns = [desc[0] for desc in self._cursor.description] if self._cursor.description else []
            result_rows = [dict(zip(columns, row)) for row in rows]
        except sqlite3.ProgrammingError:
            # No results to fetch (e.g., INSERT, UPDATE)
            result_rows = []

        return {
            "rows": result_rows,
            "rowcount": self._cursor.rowcount,
        }

    def get_stats(self) -> Dict[str, Any]:
        """
        Return statistics about the database service.
        Currently includes:
            - 'queries_executed': total number of queries run
            - 'database': the DSN used for the connection
        """
        return {
            "queries_executed": self._query_count,
            "database": getattr(self.config, "dsn", ":memory:"),
        }