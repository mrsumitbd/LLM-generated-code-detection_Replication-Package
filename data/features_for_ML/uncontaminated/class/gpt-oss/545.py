import os
import threading
from typing import Optional

class DatabaseManager:
    """Centralized database manager for PromptLab Studio.

    This class ensures that database initialization and migrations
    are handled in a centralized, thread-safe manner.
    """

    _instance: Optional["DatabaseManager"] = None
    _instance_lock = threading.Lock()

    def __new__(cls):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                # internal state
                cls._instance._init_lock = threading.Lock()
                cls._instance._initialized = False
                cls._instance._ready = False
                cls._instance._database_url = None
            return cls._instance

    def __init__(self):
        # __init__ may be called multiple times due to singleton pattern,
        # but we only want to run initialization once.
        pass

    def initialize_database(self, db_file: str) -> None:
        """Initializes the database and runs migrations.

        Args:
            db_file: Path to the SQLite database file.
        """
        with self._init_lock:
            if self._initialized:
                return
            # Ensure directory exists
            os.makedirs(os.path.dirname(os.path.abspath(db_file)), exist_ok=True)
            self._database_url = f"sqlite:///{os.path.abspath(db_file)}"
            self._run_migrations()
            self._ready = True
            self._initialized = True

    def _run_migrations(self) -> None:
        """Run database migrations.

        This is a placeholder for actual migration logic.
        """
        # In a real implementation, you would use Alembic or similar.
        # For now, we just simulate a migration step.
        pass

    @property
    def is_ready(self) -> bool:
        """Return True if the database has been initialized and migrations are complete."""
        return self._ready

    @property
    def database_url(self) -> Optional[str]:
        """Return the database URL if initialized, otherwise None."""
        return self._database_url