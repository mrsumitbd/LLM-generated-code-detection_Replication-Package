from typing import List, Optional

class MmioAccess:
    """Single MMIO read or write operation."""

    timestamp_ns: int
    operation: str  # "R" or "W"
    width: int  # 1, 2, or 4 bytes
    offset: int  # BAR-relative offset
    value: Optional[int] = None  # Value read or written