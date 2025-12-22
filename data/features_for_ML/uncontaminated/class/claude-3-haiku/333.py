import os
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List

class LogsDatabase:
    """Separate database class specifically for logs to keep logs.db separate from huntarr.db"""

    def __init__(self):
        self._logs_db_path = self._get_logs_database_path()
        self._logs_connection = self.get_logs_connection()
        self.ensure_logs_database_exists()

    def _get_logs_database_path(self) -> Path:
        return Path("logs.db")

    def _configure_logs_connection(self, conn):
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")

    def get_logs_connection(self):
        conn = sqlite3.connect(str(self._logs_db_path))
        self._configure_logs_connection(conn)
        return conn

    def _handle_logs_database_corruption(self):
        try:
            self._logs_connection.execute("SELECT COUNT(*) FROM logs;")
        except sqlite3.DatabaseError:
            os.remove(str(self._logs_db_path))
            self._logs_connection = self.get_logs_connection()

    def ensure_logs_database_exists(self):
        if not self._logs_db_path.exists():
            self._logs_connection.execute(
                """
                CREATE TABLE logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME NOT NULL,
                    level TEXT NOT NULL,
                    app_type TEXT NOT NULL,
                    message TEXT NOT NULL,
                    logger_name TEXT
                )
                """
            )
            self._logs_connection.commit()

    def insert_log(self, timestamp: datetime, level: str, app_type: str, message: str, logger_name: str = None):
        self._handle_logs_database_corruption()
        self._logs_connection.execute(
            "INSERT INTO logs (timestamp, level, app_type, message, logger_name) VALUES (?, ?, ?, ?, ?)",
            (timestamp, level, app_type, message, logger_name)
        )
        self._logs_connection.commit()

    def get_logs(self, app_type: str = None, level: str = None, limit: int = 100, offset: int = 0, search: str = None) -> List[Dict[str, Any]]:
        self._handle_logs_database_corruption()
        query = "SELECT * FROM logs"
        params = []
        if app_type:
            query += " WHERE app_type = ?"
            params.append(app_type)
        if level:
            if app_type:
                query += " AND level = ?"
            else:
                query += " WHERE level = ?"
            params.append(level)
        if search:
            if app_type or level:
                query += " AND message LIKE ?"
            else:
                query += " WHERE message LIKE ?"
            params.append(f"%{search}%")
        query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        return [dict(row) for row in self._logs_connection.execute(query, params)]

    def get_log_count(self, app_type: str = None, level: str = None, search: str = None) -> int:
        self._handle_logs_database_corruption()
        query = "SELECT COUNT(*) FROM logs"
        params = []
        if app_type:
            query += " WHERE app_type = ?"
            params.append(app_type)
        if level:
            if app_type:
                query += " AND level = ?"
            else:
                query += " WHERE level = ?"
            params.append(level)
        if search:
            if app_type or level:
                query += " AND message LIKE ?"
            else:
                query += " WHERE message LIKE ?"
            params.append(f"%{search}%")
        return self._logs_connection.execute(query, params).fetchone()[0]

    def cleanup_old_logs(self, days_to_keep: int = 30, max_entries_per_app: int = 10000):
        self._handle_logs_database_corruption()
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        self._logs_connection.execute(
            "DELETE FROM logs WHERE timestamp < ? OR (SELECT COUNT(*) FROM logs WHERE app_type = l.app_type) > ?",
            (cutoff_date, max_entries_per_app)
        )
        self._logs_connection.commit()

    def get_app_types_from_logs(self) -> List[str]:
        self._handle_logs_database_corruption()
        return [row[0] for row in self._logs_connection.execute("SELECT DISTINCT app_type FROM logs")]

    def get_log_levels(self) -> List[str]:
        self._handle_logs_database_corruption()
        return [row[0] for row in self._logs_connection.execute("SELECT DISTINCT level FROM logs")]

    def clear_logs(self, app_type: str = None):
        self._handle_logs_database_corruption()
        if app_type:
            self._logs_connection.execute("DELETE FROM logs WHERE app_type = ?", (app_type,))
        else:
            self._logs_connection.execute("DELETE FROM logs")
        self._logs_connection.commit()