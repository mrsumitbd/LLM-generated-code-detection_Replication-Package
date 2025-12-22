import os
import sqlite3
from typing import Optional

class DatabaseManager:
    """Centralized database manager for PromptLab Studio.

    This class ensures that database initialization and migrations
    are handled in a centralized, thread-safe manner.
    """

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._db_file = None
        self._conn = None
        self._is_ready = False

    def initialize_database(self, db_file: str) -> None:
        self._db_file = db_file
        if not os.path.exists(self._db_file):
            self._conn = sqlite3.connect(self._db_file)
            self._run_migrations()
            self._is_ready = True
        else:
            self._conn = sqlite3.connect(self._db_file)
            self._is_ready = True

    def _run_migrations(self) -> None:
        # Implement database migration logic here
        pass

    @property
    def is_ready(self) -> bool:
        return self._is_ready

    @property
    def database_url(self) -> Optional[str]:
        return f"sqlite:///{self._db_file}" if self._is_ready else None