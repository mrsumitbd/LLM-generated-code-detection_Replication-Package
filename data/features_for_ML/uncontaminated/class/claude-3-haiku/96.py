from typing import Dict, Any

class SyncEvent:
    """同步事件记录"""

    def __init__(self, event_id: str, event_type: str, event_time: str, event_data: Dict[str, Any]):
        self.event_id = event_id
        self.event_type = event_type
        self.event_time = event_time
        self.event_data = event_data

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "event_time": self.event_time,
            "event_data": self.event_data
        }