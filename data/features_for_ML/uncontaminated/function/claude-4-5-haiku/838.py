def get_log_timestamp_prefix(self) -> str:
    """Get timestamp prefix for consistent log filenames.

    Returns:
        Timestamp string in YYYYMMDDhhmmss format (UTC)
    """
    from datetime import datetime
    return datetime.utcnow().strftime("%Y%m%d%H%M%S")