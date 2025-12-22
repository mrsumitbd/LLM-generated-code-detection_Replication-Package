from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class WorkflowRun:
    """Immutable data transfer object for workflow context.

    This DTO safely passes workflow context data between components without
    creating tight coupling or state conflicts.
    """

    run_id: str
    name: str
    status: str
    start_time: datetime
    end_time: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Return a serialisable dictionary representation."""
        return {
            "run_id": self.run_id,
            "name": self.name,
            "status": self.status,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorkflowRun":
        """Create an instance from a dictionary."""
        return cls(
            run_id=data["run_id"],
            name=data["name"],
            status=data["status"],
            start_time=datetime.fromisoformat(data["start_time"]),
            end_time=datetime.fromisoformat(data["end_time"])
            if data.get("end_time")
            else None,
            metadata=data.get("metadata", {}),
        )

    def with_status(self, new_status: str) -> "WorkflowRun":
        """Return a new instance with an updated status."""
        return WorkflowRun(
            run_id=self.run_id,
            name=self.name,
            status=new_status,
            start_time=self.start_time,
            end_time=self.end_time,
            metadata=self.metadata,
        )

    def with_end_time(self, end_time: datetime) -> "WorkflowRun":
        """Return a new instance with an updated end time."""
        return WorkflowRun(
            run_id=self.run_id,
            name=self.name,
            status=self.status,
            start_time=self.start_time,
            end_time=end_time,
            metadata=self.metadata,
        )

    def with_metadata(self, key: str, value: Any) -> "WorkflowRun":
        """Return a new instance with an updated metadata entry."""
        new_meta = dict(self.metadata)
        new_meta[key] = value
        return WorkflowRun(
            run_id=self.run_id,
            name=self.name,
            status=self.status,
            start_time=self.start_time,
            end_time=self.end_time,
            metadata=new_meta,
        )