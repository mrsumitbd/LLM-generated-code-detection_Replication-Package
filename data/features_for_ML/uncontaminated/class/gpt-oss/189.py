from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Dict, Any


@dataclass
class TimeweaverApBonusRecord:
    """
    A record representing an Attack Power (AP) bonus granted to a Timeweaver character.
    """

    character_id: int
    """Unique identifier for the Timeweaver character."""

    bonus_amount: int
    """The amount of AP bonus granted."""

    start_time: datetime
    """Timestamp when the bonus becomes active."""

    duration: timedelta
    """How long the bonus lasts."""

    reason: Optional[str] = None
    """Optional description of why the bonus was granted."""

    # Derived fields (not part of the constructor)
    end_time: datetime = field(init=False)
    """Timestamp when the bonus expires."""

    def __post_init__(self) -> None:
        self.end_time = self.start_time + self.duration

    @property
    def is_active(self) -> bool:
        """Return True if the bonus is currently active."""
        now = datetime.utcnow()
        return self.start_time <= now < self.end_time

    @property
    def remaining(self) -> timedelta:
        """Return the remaining time before the bonus expires."""
        now = datetime.utcnow()
        if now >= self.end_time:
            return timedelta(0)
        return self.end_time - now

    def apply_to(self, base_ap: int) -> int:
        """
        Apply the bonus to a base AP value if the bonus is active.

        Parameters
        ----------
        base_ap : int
            The base attack power to which the bonus should be applied.

        Returns
        -------
        int
            The resulting attack power after applying the bonus.
        """
        if self.is_active:
            return base_ap + self.bonus_amount
        return base_ap

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the record."""
        return {
            "character_id": self.character_id,
            "bonus_amount": self.bonus_amount,
            "start_time": self.start_time.isoformat(),
            "duration_seconds": self.duration.total_seconds(),
            "end_time": self.end_time.isoformat(),
            "reason": self.reason,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TimeweaverApBonusRecord":
        """Create a record instance from a dictionary."""
        start_time = datetime.fromisoformat(data["start_time"])
        duration = timedelta(seconds=data["duration_seconds"])
        return cls(
            character_id=data["character_id"],
            bonus_amount=data["bonus_amount"],
            start_time=start_time,
            duration=duration,
            reason=data.get("reason"),
        )

    def __repr__(self) -> str:
        return (
            f"TimeweaverApBonusRecord("
            f"character_id={self.character_id!r}, "
            f"bonus_amount={self.bonus_amount!r}, "
            f"start_time={self.start_time!r}, "
            f"duration={self.duration!r}, "
            f"reason={self.reason!r})"
        )