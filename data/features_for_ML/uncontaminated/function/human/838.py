from datetime import UTC, datetime

def get_log_timestamp_prefix(self) -> str:
        """Get timestamp prefix for consistent log filenames.

        Returns:
            Timestamp string in YYYYMMDDhhmmss format (UTC)
        """
        if self.log_timestamp:
            return self.log_timestamp.strftime("%Y%m%d%H%M%S")
        else:
            # Fallback to current time if not set
            return datetime.now(UTC).strftime("%Y%m%d%H%M%S")