from datetime import datetime

def get_log_timestamp_prefix(self) -> str:
    """Get timestamp prefix for consistent log filenames.

    Returns:
        Timestamp string in YYYYMMDDhhmmss format (UTC)
    """
    return datetime.utcnow().strftime('%Y%m%d%H%M%S')