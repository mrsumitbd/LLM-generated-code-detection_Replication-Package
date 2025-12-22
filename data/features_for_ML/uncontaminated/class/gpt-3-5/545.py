from typing import Optional

class DatabaseManager:
    """Centralized database manager for PromptLab Studio.

    This class ensures that database initialization and migrations
    are handled in a centralized, thread-safe manner.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._is_ready = False
        self._database_url = None

    def initialize_database(self, db_file: str) -> None:
        # Initialize database logic here
        self._run_migrations()
        self._is_ready = True
        self._database_url = db_file

    def _run_migrations(self) -> None:
        # Run migrations logic here
        pass

    @property
    def is_ready(self) -> bool:
        return self._is_ready

    @property
    def database_url(self) -> Optional[str]:
        return self._database_url