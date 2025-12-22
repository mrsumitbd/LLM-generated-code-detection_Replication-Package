import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

class LogsDatabase:
    """Separate database class specifically for logs to keep logs.db separate from huntarr.db"""

    def __init__(self):
        self._db_path = self._get_logs_database_path()
        self.ensure_logs_database_exists()

    def _get_logs_database_path(self) -> Path:
        """Return the absolute path to the logs database file."""
        return Path(__file__).parent / "logs.db"

    def _configure_logs_connection(self, conn: sqlite3.Connection) -> None:
        """Configure the SQLite connection for logs."""
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")

    def get_logs_connection(self) -> sqlite3.Connection:
        """Return a new SQLite connection configured for logs."""
        conn = sqlite3.connect(str(self._db_path), timeout=30.0, isolation_level=None)
        self._configure_logs_connection(conn)
        return conn

    def _handle_logs_database_corruption(self) -> None:
        """Handle a corrupted logs database by deleting and recreating it."""
        try:
            # Close any existing connections
            pass
        finally:
            if self._db_path.exists():
                self._db_path.unlink()
            self.ensure_logs_database_exists()

    def ensure_logs_database_exists(self) -> None:
        """Create the logs database and table if they do not exist."""
        try:
            with self.get_logs_connection() as conn:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        level TEXT NOT NULL,
                        app_type TEXT NOT NULL,
                        message TEXT NOT NULL,
                        logger_name TEXT
                    );
                    """
                )
                conn.execute("CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON logs(timestamp);")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_logs_app_type ON logs(app_type);")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_logs_level ON logs(level);")
        except sqlite3.DatabaseError:
            self._handle_logs_database_corruption()

    def insert_log(
        self,
        timestamp: datetime,
        level: str,
        app_type: str,
        message: str,
        logger_name: Optional[str] = None,
    ) -> None:
        """Insert a log entry into the database."""
        try:
            with self.get_logs_connection() as conn:
                conn.execute(
                    """
                    INSERT INTO logs (timestamp, level, app_type, message, logger_name)
                    VALUES (?, ?, ?, ?, ?);
                    """,
                    (
                        timestamp.isoformat(),
                        level,
                        app_type,
                        message,
                        logger_name,
                    ),
                )
        except sqlite3.DatabaseError:
            self._handle_logs_database_corruption()

    def get_logs(
        self,
        app_type: Optional[str] = None,
        level: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
        search: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Retrieve logs with optional filtering, pagination, and search."""
        try:
            with self.get_logs_connection() as conn:
                query = "SELECT * FROM logs"
                conditions = []
                params: List[Any] = []

                if app_type:
                    conditions.append("app_type = ?")
                    params.append(app_type)
                if level:
                    conditions.append("level = ?")
                    params.append(level)
                if search:
                    conditions.append("(message LIKE ? OR logger_name LIKE ?)")
                    params.extend([f"%{search}%", f"%{search}%"])

                if conditions:
                    query += " WHERE " + " AND ".join(conditions)

                query += " ORDER BY timestamp DESC"
                query += " LIMIT ? OFFSET ?"
                params.extend([limit, offset])

                cursor = conn.execute(query, params)
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except sqlite3.DatabaseError:
            self._handle_logs_database_corruption()
            return []

    def get_log_count(
        self,
        app_type: Optional[str] = None,
        level: Optional[str] = None,
        search: Optional[str] = None,
    ) -> int:
        """Return the count of logs matching the optional filters."""
        try:
            with self.get_logs_connection() as conn:
                query = "SELECT COUNT(*) AS cnt FROM logs"
                conditions = []
                params: List[Any] = []

                if app_type:
                    conditions.append("app_type = ?")
                    params.append(app_type)
                if level:
                    conditions.append("level = ?")
                    params.append(level)
                if search:
                    conditions.append("(message LIKE ? OR logger_name LIKE ?)")
                    params.extend([f"%{search}%", f"%{search}%"])

                if conditions:
                    query += " WHERE " + " AND ".join(conditions)

                cursor = conn.execute(query, params)
                row = cursor.fetchone()
                return row["cnt"] if row else 0
        except sqlite3.DatabaseError:
            self._handle_logs_database_corruption()
            return 0

    def cleanup_old_logs(self, days_to_keep: int = 30, max_entries_per_app: int = 10000) -> None:
        """Delete logs older than `days_to_keep` and enforce a maximum number of entries per app."""
        cutoff = datetime.utcnow() - timedelta(days=days_to_keep)
        try:
            with self.get_logs_connection() as conn:
                # Delete old logs
                conn.execute(
                    "DELETE FROM logs WHERE timestamp < ?;",
                    (cutoff.isoformat(),),
                )

                # Enforce max entries per app
                app_types = self.get_app_types_from_logs()
                for app in app_types:
                    # Count entries for this app
                    cursor = conn.execute(
                        "SELECT COUNT(*) AS cnt FROM logs WHERE app_type = ?;",
                        (app,),
                    )
                    row = cursor.fetchone()
                    count = row["cnt"] if row else 0
                    if count > max_entries_per_app:
                        # Delete the oldest entries beyond the limit
                        to_delete = count - max_entries_per_app
                        conn.execute(
                            """
                            DELETE FROM logs
                            WHERE id IN (
                                SELECT id FROM logs
                                WHERE app_type = ?
                                ORDER BY timestamp ASC
                                LIMIT ?
                            );
                            """,
                            (app, to_delete),
                        )
        except sqlite3.DatabaseError:
            self._handle_logs_database_corruption()

    def get_app_types_from_logs(self) -> List[str]:
        """Return a list of distinct app types present in the logs."""
        try:
            with self.get_logs_connection() as conn:
                cursor = conn.execute("SELECT DISTINCT app_type FROM logs;")
                return [row["app_type"] for row in cursor.fetchall()]
        except sqlite3.DatabaseError:
            self._handle_logs_database_corruption()
            return []

    def get_log_levels(self) -> List[str]:
        """Return a list of distinct log levels present in the logs."""
        try:
            with self.get_logs_connection() as conn:
                cursor = conn.execute("SELECT DISTINCT level FROM logs;")
                return [row["level"] for row in cursor.fetchall()]
        except sqlite3.DatabaseError:
            self._handle_logs_database_corruption()
            return []

    def clear_logs(self, app_type: Optional[str] = None) -> None:
        """Delete all logs or logs for a specific app type."""
        try:
            with self.get_logs_connection() as conn:
                if app_type:
                    conn.execute("DELETE FROM logs WHERE app_type = ?;", (app_type,))
                else:
                    conn.execute("DELETE FROM logs;")
        except sqlite3.DatabaseError:
            self._handle_logs_database_corruption()