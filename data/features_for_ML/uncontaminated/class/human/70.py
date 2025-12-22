from datetime import datetime, timedelta

class StorageInfo:
    """Storage information structure."""

    total_space: int
    used_space: int
    free_space: int
    usage_percentage: float
    warning_level: StorageWarningLevel
    last_updated: datetime