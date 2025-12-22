import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import time

class TableInfo:
    name: str
    database: str
    size_bytes: int = 0
    size_str: str = ""
    replica_count: int = 0
    columns: List[ColumnInfo] = field(default_factory=list)
    create_statement: Optional[str] = None
    last_updated: float = 0
    error_message: Optional[str] = None
    
    def __post_init__(self):
        if not self.last_updated:
            self.last_updated = time.time()
    
    @staticmethod
    def parse_size_string(size_str: str) -> int:
        """Parse size strings like '1.285 GB', '714.433 MB', '2.269 KB' to bytes"""
        if not size_str or size_str == "0" or size_str.lower() == "total":
            return 0
            
        # Handle special cases
        if size_str.lower() in ["quota", "left"]:
            return 0
            
        # Match pattern like "1.285 GB"
        match = re.match(r'([\d.]+)\s*([KMGT]?B)', size_str.strip(), re.IGNORECASE)
        if not match:
            return 0
            
        value, unit = match.groups()
        try:
            num_value = float(value)
        except ValueError:
            return 0
            
        multipliers = {
            'B': 1,
            'KB': 1024,
            'MB': 1024 ** 2,
            'GB': 1024 ** 3,
            'TB': 1024 ** 4
        }
        
        multiplier = multipliers.get(unit.upper(), 1)
        return int(num_value * multiplier)
    
    def is_large_table(self) -> bool:
        """Determine if table is considered large (replica_count > 64 OR size > 2GB)"""
        return self.replica_count > 64 or self.size_bytes > (2 * 1024 ** 3)
    
    def priority_score(self) -> float:
        """Calculate priority score combining size and replica count for sorting"""
        # Normalize size to GB and combine with replica count
        size_gb = self.size_bytes / (1024 ** 3)
        return size_gb + (self.replica_count * 0.1)  # Weight replica count less than size
    
    def is_expired(self, expire_seconds: int = 120) -> bool:
        """Check if cache entry is expired (default 2 minutes)"""
        return time.time() - self.last_updated > expire_seconds