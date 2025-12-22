class LogDetail:
    """Standardized log detail structure."""
    
    def __init__(self, timestamp, message, log_level):
        self.timestamp = timestamp
        self.message = message
        self.log_level = log_level
        
    def __str__(self):
        return f"{self.timestamp} - [{self.log_level}] {self.message}"