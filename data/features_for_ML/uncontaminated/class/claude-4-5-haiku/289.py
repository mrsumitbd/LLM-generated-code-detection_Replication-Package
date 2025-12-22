from dataclasses import dataclass
from datetime import datetime, timedelta
import re

@dataclass
class TableInfo:
    name: str
    size: str
    last_accessed: datetime
    row_count: int = 0
    
    def __post_init__(self):
        if isinstance(self.size, str):
            self.size_bytes = self.parse_size_string(self.size)
        else:
            self.size_bytes = self.size
        
        if isinstance(self.last_accessed, str):
            self.last_accessed = datetime.fromisoformat(self.last_accessed)

    @staticmethod
    def parse_size_string(size_str: str) -> int:
        size_str = size_str.strip().upper()
        
        units = {
            'B': 1,
            'KB': 1024,
            'MB': 1024 ** 2,
            'GB': 1024 ** 3,
            'TB': 1024 ** 4,
        }
        
        match = re.match(r'([\d.]+)\s*([A-Z]+)', size_str)
        if not match:
            return 0
        
        value = float(match.group(1))
        unit = match.group(2)
        
        multiplier = units.get(unit, 1)
        return int(value * multiplier)

    def is_large_table(self) -> bool:
        return self.size_bytes > 1024 ** 3

    def priority_score(self) -> float:
        size_score = min(self.size_bytes / (1024 ** 3), 10.0)
        
        time_diff = datetime.now() - self.last_accessed
        access_score = min(time_diff.total_seconds() / 3600, 10.0)
        
        row_score = min(self.row_count / 1000000, 10.0)
        
        priority = (size_score * 0.5) + (access_score * 0.3) + (row_score * 0.2)
        return priority

    def is_expired(self, expire_seconds: int = 120) -> bool:
        time_diff = datetime.now() - self.last_accessed
        return time_diff.total_seconds() > expire_seconds