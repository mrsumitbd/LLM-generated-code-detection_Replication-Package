from typing import Dict, Any

class SyncEvent:
    """同步事件记录"""

    def __init__(self, event_type: str, timestamp: int):
        self.event_type = event_type
        self.timestamp = timestamp

    def to_dict(self) -> Dict[str, Any]:
        return {
            'event_type': self.event_type,
            'timestamp': self.timestamp
        }