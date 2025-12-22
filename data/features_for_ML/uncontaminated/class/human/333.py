import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
import platform
import platform
import time
import datetime
import time
from pathlib import Path
from datetime import datetime, timedelta
import platform
import sqlite3
import time
import time
import time
import datetime
from datetime import datetime
from datetime import datetime, timedelta
import time
from datetime import datetime, timedelta
import time
import time
import time
import time
import datetime

class LogsDatabase:
    """Separate database class specifically for logs to keep logs.db separate from huntarr.db"""
    
    def __init__(self):
        self.db_path = self._get_logs_database_path()
        self.ensure_logs_database_exists()
    
    def _get_logs_database_path(self) -> Path:
        """Get logs database path - same directory as main database but separate file"""
        # Check if running in Docker
        config_dir = Path("/config")
        if config_dir.exists() and config_dir.is_dir():
            return config_dir / "logs.db"
        
        # Check for Windows config directory
        windows_config = os.environ.get("HUNTARR_CONFIG_DIR")
        if windows_config:
            config_path = Path(windows_config)
            config_path.mkdir(parents=True, exist_ok=True)
            return config_path / "logs.db"
        
        # Check for Windows AppData
        import platform
        if platform.system() == "Windows":
            appdata = os.environ.get("APPDATA", os.path.expanduser("~"))
            windows_config_dir = Path(appdata) / "Huntarr"
            windows_config_dir.mkdir(parents=True, exist_ok=True)
            return windows_config_dir / "logs.db"
        
        # Local development
        project_root = Path(__file__).parent.parent.parent.parent
        data_dir = project_root / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir / "logs.db"
    
    def _configure_logs_connection(self, conn):
        """Configure SQLite connection optimized for high-volume log writes"""
        try:
            conn.execute('PRAGMA foreign_keys = ON')
            
            # WAL mode is particularly beneficial for logs (write-heavy workload)
            try:
                conn.execute('PRAGMA journal_mode = WAL')
            except Exception as wal_error:
                logger.warning(f"WAL mode failed for logs.db, using DELETE mode: {wal_error}")
                conn.execute('PRAGMA journal_mode = DELETE')
            
            # Optimized settings for log writing
            conn.execute('PRAGMA synchronous = NORMAL')     # Balance between speed and safety for logs
            conn.execute('PRAGMA cache_size = -16000')      # 16MB cache for log operations
            conn.execute('PRAGMA temp_store = MEMORY')
            conn.execute('PRAGMA busy_timeout = 30000')     # 30 seconds for log operations
            conn.execute('PRAGMA auto_vacuum = INCREMENTAL')
            
            # WAL-specific optimizations for logs
            result = conn.execute('PRAGMA journal_mode').fetchone()
            if result and result[0] == 'wal':
                conn.execute('PRAGMA wal_autocheckpoint = 2000')    # Less frequent checkpoints for logs
                conn.execute('PRAGMA journal_size_limit = 134217728') # 128MB journal size for logs
                
        except Exception as e:
            logger.error(f"Error configuring logs database connection: {e}")
            pass
    
    def get_logs_connection(self):
        """Get a configured SQLite connection for logs database"""
        try:
            conn = sqlite3.connect(self.db_path)
            self._configure_logs_connection(conn)
            # Test connection
            conn.execute("SELECT name FROM sqlite_master WHERE type='table' LIMIT 1").fetchone()
            return conn
        except (sqlite3.DatabaseError, sqlite3.OperationalError) as e:
            if "file is not a database" in str(e) or "database disk image is malformed" in str(e):
                logger.error(f"Logs database corruption detected: {e}")
                self._handle_logs_database_corruption()
                # Try connecting again after recovery
                conn = sqlite3.connect(self.db_path)
                self._configure_logs_connection(conn)
                return conn
            else:
                raise
    
    def _handle_logs_database_corruption(self):
        """Handle logs database corruption"""
        import time
        
        logger.error(f"Handling logs database corruption for: {self.db_path}")
        
        try:
            if self.db_path.exists():
                backup_path = self.db_path.parent / f"logs_corrupted_backup_{int(time.time())}.db"
                self.db_path.rename(backup_path)
                logger.warning(f"Corrupted logs database backed up to: {backup_path}")
                logger.warning("Starting with fresh logs database - log history will be lost")
            
            if self.db_path.exists():
                self.db_path.unlink()
                
        except Exception as backup_error:
            logger.error(f"Error during logs database corruption recovery: {backup_error}")
            try:
                if self.db_path.exists():
                    self.db_path.unlink()
            except:
                pass
    
    def ensure_logs_database_exists(self):
        """Create logs database and tables if they don't exist"""
        try:
            with self.get_logs_connection() as conn:
                # Create logs table
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp DATETIME NOT NULL,
                        level TEXT NOT NULL,
                        app_type TEXT NOT NULL,
                        message TEXT NOT NULL,
                        logger_name TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create indexes for logs performance
                conn.execute('CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON logs(timestamp)')
                conn.execute('CREATE INDEX IF NOT EXISTS idx_logs_app_type ON logs(app_type)')
                conn.execute('CREATE INDEX IF NOT EXISTS idx_logs_level ON logs(level)')
                conn.execute('CREATE INDEX IF NOT EXISTS idx_logs_app_level ON logs(app_type, level)')
                
                conn.commit()
                logger.info(f"Logs database initialized at: {self.db_path}")
                
        except (sqlite3.DatabaseError, sqlite3.OperationalError) as e:
            if "file is not a database" in str(e) or "database disk image is malformed" in str(e):
                logger.error(f"Logs database corruption detected during table creation: {e}")
                self._handle_logs_database_corruption()
                # Try creating tables again after recovery
                self.ensure_logs_database_exists()
            else:
                raise
    
    def insert_log(self, timestamp: datetime, level: str, app_type: str, message: str, logger_name: str = None):
        """Insert a log entry into the logs database"""
        try:
            with self.get_logs_connection() as conn:
                conn.execute('''
                    INSERT INTO logs (timestamp, level, app_type, message, logger_name)
                    VALUES (?, ?, ?, ?, ?)
                ''', (timestamp, level, app_type, message, logger_name))
                conn.commit()
        except Exception as e:
            # Don't let log insertion failures crash the app
            print(f"Error inserting log: {e}")
    
    def get_logs(self, app_type: str = None, level: str = None, limit: int = 100, offset: int = 0, search: str = None) -> List[Dict[str, Any]]:
        """Get logs with filtering and pagination"""
        try:
            with self.get_logs_connection() as conn:
                conn.row_factory = sqlite3.Row
                
                where_conditions = []
                params = []
                
                if app_type and app_type != "all":
                    where_conditions.append("app_type = ?")
                    params.append(app_type)
                
                if level and level != "all":
                    where_conditions.append("level = ?")
                    params.append(level)
                
                if search:
                    where_conditions.append("message LIKE ?")
                    params.append(f"%{search}%")
                
                where_clause = "WHERE " + " AND ".join(where_conditions) if where_conditions else ""
                
                query = f"""
                    SELECT * FROM logs {where_clause}
                    ORDER BY timestamp DESC
                    LIMIT ? OFFSET ?
                """
                
                cursor = conn.execute(query, params + [limit, offset])
                return [dict(row) for row in cursor.fetchall()]
                
        except Exception as e:
            logger.error(f"Error getting logs: {e}")
            return []
    
    def get_log_count(self, app_type: str = None, level: str = None, search: str = None) -> int:
        """Get total count of logs matching filters"""
        try:
            with self.get_logs_connection() as conn:
                where_conditions = []
                params = []
                
                if app_type and app_type != "all":
                    where_conditions.append("app_type = ?")
                    params.append(app_type)
                
                if level and level != "all":
                    where_conditions.append("level = ?")
                    params.append(level)
                
                if search:
                    where_conditions.append("message LIKE ?")
                    params.append(f"%{search}%")
                
                where_clause = "WHERE " + " AND ".join(where_conditions) if where_conditions else ""
                
                query = f"SELECT COUNT(*) FROM logs {where_clause}"
                cursor = conn.execute(query, params)
                return cursor.fetchone()[0]
                
        except Exception as e:
            logger.error(f"Error getting log count: {e}")
            return 0
    
    def cleanup_old_logs(self, days_to_keep: int = 30, max_entries_per_app: int = 10000):
        """Clean up old logs to prevent database bloat"""
        try:
            with self.get_logs_connection() as conn:
                # Delete logs older than specified days
                cutoff_date = datetime.now() - timedelta(days=days_to_keep)
                cursor = conn.execute("DELETE FROM logs WHERE timestamp < ?", (cutoff_date,))
                deleted_by_age = cursor.rowcount
                
                # Keep only the most recent entries per app
                apps_cursor = conn.execute("SELECT DISTINCT app_type FROM logs")
                total_deleted_by_count = 0
                
                for (app_type,) in apps_cursor.fetchall():
                    # Get count for this app
                    count_cursor = conn.execute("SELECT COUNT(*) FROM logs WHERE app_type = ?", (app_type,))
                    count = count_cursor.fetchone()[0]
                    
                    if count > max_entries_per_app:
                        # Delete oldest entries beyond the limit
                        excess_count = count - max_entries_per_app
                        delete_cursor = conn.execute("""
                            DELETE FROM logs 
                            WHERE app_type = ? 
                            AND id IN (
                                SELECT id FROM logs 
                                WHERE app_type = ? 
                                ORDER BY timestamp ASC 
                                LIMIT ?
                            )
                        """, (app_type, app_type, excess_count))
                        total_deleted_by_count += delete_cursor.rowcount
                
                conn.commit()
                return deleted_by_age + total_deleted_by_count
                
        except Exception as e:
            logger.error(f"Error cleaning up logs: {e}")
            return 0
    
    def get_app_types_from_logs(self) -> List[str]:
        """Get list of all app types that have logs"""
        try:
            with self.get_logs_connection() as conn:
                cursor = conn.execute("SELECT DISTINCT app_type FROM logs ORDER BY app_type")
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting app types from logs: {e}")
            return []
    
    def get_log_levels(self) -> List[str]:
        """Get list of all log levels that exist"""
        try:
            with self.get_logs_connection() as conn:
                cursor = conn.execute("SELECT DISTINCT level FROM logs ORDER BY level")
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting log levels: {e}")
            return []
    
    def clear_logs(self, app_type: str = None):
        """Clear logs for a specific app type or all logs"""
        try:
            with self.get_logs_connection() as conn:
                if app_type:
                    cursor = conn.execute("DELETE FROM logs WHERE app_type = ?", (app_type,))
                else:
                    cursor = conn.execute("DELETE FROM logs")
                
                deleted_count = cursor.rowcount
                conn.commit()
                
                logger.info(f"Cleared {deleted_count} logs" + (f" for {app_type}" if app_type else ""))
                return deleted_count
        except Exception as e:
            logger.error(f"Error clearing logs: {e}")
            return 0