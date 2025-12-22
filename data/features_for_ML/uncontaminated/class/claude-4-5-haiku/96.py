from typing import Dict, Any
from datetime import datetime

class SyncEvent:
    """同步事件记录"""

    def __init__(self, event_type: str, timestamp: datetime = None, source: str = None, 
                 target: str = None, status: str = None, details: Dict[str, Any] = None):
        self.event_type = event_type
        self.timestamp = timestamp or datetime.now()
        self.source = source
        self.target = target
        self.status = status
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            'event_type': self.event_type,
            'timestamp': self.timestamp.isoformat() if isinstance(self.timestamp, datetime) else self.timestamp,
            'source': self.source,
            'target': self.target,
            'status': self.status,
            'details': self.details
        }