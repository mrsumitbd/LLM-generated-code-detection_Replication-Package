import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging

class LogsDatabase:
    """Separate database class specifically for logs to keep logs.db separate from huntarr.db"""

    def __init__(self):
        self.db_path = self._get_logs_database_path()
        self.ensure_logs_database_exists()

    def _get_logs_database_path(self) -> Path:
        db_dir = Path.home() / ".huntarr"
        db_dir.mkdir(parents=True, exist_ok=True)
        return db_dir / "logs.db"

    def _configure_logs_connection(self, conn):
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA cache_size=10000")
        return conn

    def get_logs_connection(self):
        try:
            conn = sqlite3.connect(str(self.db_path), timeout=10.0)
            return self._configure_logs_connection(conn)
        except sqlite3.DatabaseError:
            self._handle_logs_database_corruption()
            conn = sqlite3.connect(str(self.db_path), timeout=10.0)
            return self._configure_logs_connection(conn)

    def _handle_logs_database_corruption(self):
        try:
            if self.db_path.exists():
                backup_path = self.db_path.with_suffix('.db.corrupt')
                self.db_path.rename(backup_path)
        except Exception as e:
            logging.error(f"Error handling logs database corruption: {e}")

    def ensure_logs_database_exists(self):
        conn = self.get_logs_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME NOT NULL,
                    level TEXT NOT NULL,
                    app_type TEXT NOT NULL,
                    message TEXT NOT NULL,
                    logger_name TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_logs_timestamp 
                ON logs(timestamp DESC)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_logs_app_type 
                ON logs(app_type)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_logs_level 
                ON logs(level)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_logs_app_level 
                ON logs(app_type, level)
            """)
            conn.commit()
        finally:
            conn.close()

    def insert_log(self, timestamp: datetime, level: str, app_type: str, message: str, logger_name: str = None):
        conn = self.get_logs_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO logs (timestamp, level, app_type, message, logger_name)
                VALUES (?, ?, ?, ?, ?)
            """, (timestamp, level, app_type, message, logger_name))
            conn.commit()
        finally:
            conn.close()

    def get_logs(self, app_type: str = None, level: str = None, limit: int = 100, offset: int = 0, search: str = None) -> List[Dict[str, Any]]:
        conn = self.get_logs_connection()
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM logs WHERE 1=1"
            params = []

            if app_type:
                query += " AND app_type = ?"
                params.append(app_type)

            if level:
                query += " AND level = ?"
                params.append(level)

            if search:
                query += " AND (message LIKE ? OR logger_name LIKE ?)"
                search_param = f"%{search}%"
                params.extend([search_param, search_param])

            query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])

            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    def get_log_count(self, app_type: str = None, level: str = None, search: str = None) -> int:
        conn = self.get_logs_connection()
        try:
            cursor = conn.cursor()
            query = "SELECT COUNT(*) as count FROM logs WHERE 1=1"
            params = []

            if app_type:
                query += " AND app_type = ?"
                params.append(app_type)

            if level:
                query += " AND level = ?"
                params.append(level)

            if search:
                query += " AND (message LIKE ? OR logger_name LIKE ?)"
                search_param = f"%{search}%"
                params.extend([search_param, search_param])

            cursor.execute(query, params)
            result = cursor.fetchone()
            return result['count'] if result else 0
        finally:
            conn.close()

    def cleanup_old_logs(self, days_to_keep: int = 30, max_entries_per_app: int = 10000):
        conn = self.get_logs_connection()
        try:
            cursor = conn.cursor()
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)

            cursor.execute("""
                DELETE FROM logs 
                WHERE timestamp < ?
            """, (cutoff_date,))

            cursor.execute("""
                SELECT app_type, COUNT(*) as count 
                FROM logs 
                GROUP BY app_type 
                HAVING count > ?
            """, (max_entries_per_app,))

            app_types = cursor.fetchall()
            for row in app_types:
                app_type = row['app_type']
                excess_count = row['count'] - max_entries_per_app

                cursor.execute("""
                    DELETE FROM logs 
                    WHERE app_type = ? 
                    AND id IN (
                        SELECT id FROM logs 
                        WHERE app_type = ? 
                        ORDER BY timestamp ASC 
                        LIMIT ?
                    )
                """, (app_type, app_type, excess_count))

            conn.commit()
        finally:
            conn.close()

    def get_app_types_from_logs(self) -> List[str]:
        conn = self.get_logs_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT app_type FROM logs ORDER BY app_type")
            rows = cursor.fetchall()
            return [row['app_type'] for row in rows]
        finally:
            conn.close()

    def get_log_levels(self) -> List[str]:
        return ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    def clear_logs(self, app_type: str = None):
        conn = self.get_logs_connection()
        try:
            cursor = conn.cursor()
            if app_type:
                cursor.execute("DELETE FROM logs WHERE app_type = ?", (app_type,))
            else:
                cursor.execute("DELETE FROM logs")
            conn.commit()
        finally:
            conn.close()