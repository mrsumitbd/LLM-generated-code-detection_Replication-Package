from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional


class SyncEvent:
    """同步事件记录"""

    def __init__(
        self,
        event_id: str,
        timestamp: datetime | str,
        status: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.event_id = event_id
        self.timestamp = (
            timestamp if isinstance(timestamp, datetime) else datetime.fromisoformat(timestamp)
        )
        self.status = status
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status,
            "details": self.details,
        }

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"event_id={self.event_id!r}, "
            f"timestamp={self.timestamp.isoformat()!r}, "
            f"status={self.status!r}, "
            f"details={self.details!r})"
        )