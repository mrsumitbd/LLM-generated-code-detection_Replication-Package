class DatabaseManager:
    """Centralized database manager for PromptLab Studio.

    This class ensures that database initialization and migrations
    are handled in a centralized, thread-safe manner.
    """

    _instance = None
    _lock = __import__('threading').Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self._db_file = None
        self._db_url = None
        self._is_ready = False
        self._initialized = True

    def initialize_database(self, db_file: str) -> None:
        import os
        from pathlib import Path
        
        db_path = Path(db_file)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self._db_file = str(db_path)
        self._db_url = f"sqlite:///{self._db_file}"
        
        self._run_migrations()
        self._is_ready = True

    def _run_migrations(self) -> None:
        import sqlite3
        
        if not self._db_file:
            raise RuntimeError("Database file not set. Call initialize_database first.")
        
        conn = sqlite3.connect(self._db_file)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS migrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()

    @property
    def is_ready(self) -> bool:
        return self._is_ready

    @property
    def database_url(self) -> 'Optional[str]':
        return self._db_url