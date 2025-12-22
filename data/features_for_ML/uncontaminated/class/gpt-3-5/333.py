from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path

class LogsDatabase:
    """Separate database class specifically for logs to keep logs.db separate from huntarr.db"""

    def __init__(self):
        pass

    def _get_logs_database_path(self) -> Path:
        pass

    def _configure_logs_connection(self, conn):
        pass

    def get_logs_connection(self):
        pass

    def _handle_logs_database_corruption(self):
        pass

    def ensure_logs_database_exists(self):
        pass

    def insert_log(self, timestamp: datetime, level: str, app_type: str, message: str, logger_name: str = None):
        pass

    def get_logs(self, app_type: str = None, level: str = None, limit: int = 100, offset: int = 0, search: str = None) -> List[Dict[str, Any]]:
        pass

    def get_log_count(self, app_type: str = None, level: str = None, search: str = None) -> int:
        pass

    def cleanup_old_logs(self, days_to_keep: int = 30, max_entries_per_app: int = 10000):
        pass

    def get_app_types_from_logs(self) -> List[str]:
        pass

    def get_log_levels(self) -> List[str]:
        pass

    def clear_logs(self, app_type: str = None):
        pass