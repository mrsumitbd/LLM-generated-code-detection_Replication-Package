from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any


@dataclass(slots=True)
class ComplianceRequirement:
    """Individual compliance requirement."""

    requirement_id: str
    title: str
    description: str = ""
    status: str = "pending"  # allowed: pending, met, not_met
    evidence: List[str] = field(default_factory=list)
    due_date: Optional[datetime] = None

    _ALLOWED_STATUS = {"pending", "met", "not_met"}

    def __post_init__(self) -> None:
        if self.status not in self._ALLOWED_STATUS:
            raise ValueError(
                f"status must be one of {self._ALLOWED_STATUS}, got {self.status!r}"
            )
        if self.due_date is not None and not isinstance(self.due_date, datetime):
            raise TypeError("due_date must be a datetime instance or None")

    # ------------------------------------------------------------------
    # Basic property helpers
    # ------------------------------------------------------------------
    @property
    def is_met(self) -> bool:
        """Return True if the requirement is satisfied."""
        return self.status == "met"

    @property
    def is_overdue(self) -> bool:
        """Return True if the due date has passed and the requirement is not met."""
        if self.due_date is None:
            return False
        return datetime.utcnow() > self.due_date and not self.is_met

    @property
    def days_until_due(self) -> Optional[int]:
        """Return the number of days until the due date, or None if no due date."""
        if self.due_date is None:
            return None
        delta = self.due_date - datetime.utcnow()
        return max(delta.days, 0)

    # ------------------------------------------------------------------
    # Mutating methods
    # ------------------------------------------------------------------
    def add_evidence(self, evidence_item: str) -> None:
        """Add an evidence item to the requirement."""
        if not evidence_item:
            raise ValueError("evidence_item must be a non-empty string")
        self.evidence.append(evidence_item)

    def set_status(self, new_status: str) -> None:
        """Set the compliance status."""
        if new_status not in self._ALLOWED_STATUS:
            raise ValueError(
                f"new_status must be one of {self._ALLOWED_STATUS}, got {new_status!r}"
            )
        self.status = new_status

    # ------------------------------------------------------------------
    # Serialization helpers
    # ------------------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        """Return a serializable dictionary representation."""
        data = asdict(self)
        # Convert datetime to ISO format
        if self.due_date is not None:
            data["due_date"] = self.due_date.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ComplianceRequirement":
        """Create an instance from a dictionary."""
        due = data.get("due_date")
        if due is not None:
            data = data.copy()
            data["due_date"] = datetime.fromisoformat(due)
        return cls(**data)

    def to_json(self) -> str:
        """Return a JSON string representation."""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> "ComplianceRequirement":
        """Create an instance from a JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)

    # ------------------------------------------------------------------
    # Convenience methods
    # ------------------------------------------------------------------
    def evidence_count(self) -> int:
        """Return the number of evidence items."""
        return len(self.evidence)

    def summary(self) -> str:
        """Return a short summary string."""
        status = "Met" if self.is_met else "Not Met" if self.status == "not_met" else "Pending"
        due = self.due_date.isoformat() if self.due_date else "No due date"
        return (
            f"[{self.requirement_id}] {self.title} - {status} - Due: {due} "
            f"({self.evidence_count()} evidence items)"
        )

    # ------------------------------------------------------------------
    # Rich comparison and representation
    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"ComplianceRequirement(requirement_id={self.requirement_id!r}, "
            f"title={self.title!r}, status={self.status!r}, "
            f"evidence={self.evidence!r}, due_date={self.due_date!r})"
        )

    def __str__(self) -> str:
        return self.summary()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ComplianceRequirement):
            return NotImplemented
        return (
            self.requirement_id == other.requirement_id
            and self.title == other.title
            and self.description == other.description
            and self.status == other.status
            and self.evidence == other.evidence
            and self.due_date == other.due_date
        )

    def __hash__(self) -> int:
        return hash(
            (
                self.requirement_id,
                self.title,
                self.description,
                self.status,
                tuple(self.evidence),
                self.due_date,
            )
        )

    # ------------------------------------------------------------------
    # Iterable and container protocol
    # ------------------------------------------------------------------
    def __iter__(self):
        """Iterate over the attribute names."""
        for field_name in self.__dataclass_fields__:
            yield getattr(self, field_name)

    def __len__(self) -> int:
        """Return the number of attributes."""
        return len(self.__dataclass_fields__)

    def __contains__(self, item: str) -> bool:
        """Check if an attribute name exists."""
        return item in self.__dataclass_fields__

    def __getitem__(self, key: str) -> Any:
        """Get an attribute by name."""
        if key not in self.__dataclass_fields__:
            raise KeyError(key)
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any) -> None:
        """Set an attribute by name."""
        if key not in self.__dataclass_fields__:
            raise KeyError(key)
        setattr(self, key, value)