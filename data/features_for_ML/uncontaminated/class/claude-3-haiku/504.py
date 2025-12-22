class LogDetail:
    """Standardized log detail structure."""

    def __init__(self, timestamp, level, message, source=None, data=None):
        self.timestamp = timestamp
        self.level = level
        self.message = message
        self.source = source
        self.data = data

    def __str__(self):
        log_detail_str = f"Timestamp: {self.timestamp}\nLevel: {self.level}\nMessage: {self.message}"
        if self.source:
            log_detail_str += f"\nSource: {self.source}"
        if self.data:
            log_detail_str += f"\nData: {self.data}"
        return log_detail_str

    def __repr__(self):
        return f"LogDetail(timestamp='{self.timestamp}', level='{self.level}', message='{self.message}', source='{self.source}', data='{self.data}')"