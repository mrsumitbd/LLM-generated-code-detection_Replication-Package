class StorageInfo:
    """Storage information structure."""
    
    def __init__(self, name: str, size: int, used: int, available: int, percent: float):
        """Initialize StorageInfo with storage details.
        
        Args:
            name: Name/path of the storage device
            size: Total size in bytes
            used: Used space in bytes
            available: Available space in bytes
            percent: Percentage of storage used
        """
        self.name = name
        self.size = size
        self.used = used
        self.available = available
        self.percent = percent
    
    def __repr__(self) -> str:
        """Return string representation of StorageInfo."""
        return (f"StorageInfo(name={self.name!r}, size={self.size}, "
                f"used={self.used}, available={self.available}, percent={self.percent})")
    
    def __str__(self) -> str:
        """Return human-readable string representation."""
        return (f"Storage: {self.name}\n"
                f"  Total: {self._format_bytes(self.size)}\n"
                f"  Used: {self._format_bytes(self.used)} ({self.percent}%)\n"
                f"  Available: {self._format_bytes(self.available)}")
    
    @staticmethod
    def _format_bytes(bytes_value: int) -> str:
        """Format bytes to human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024
        return f"{bytes_value:.2f} PB"
    
    def to_dict(self) -> dict:
        """Convert StorageInfo to dictionary."""
        return {
            'name': self.name,
            'size': self.size,
            'used': self.used,
            'available': self.available,
            'percent': self.percent
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'StorageInfo':
        """Create StorageInfo from dictionary."""
        return cls(
            name=data['name'],
            size=data['size'],
            used=data['used'],
            available=data['available'],
            percent=data['percent']
        )