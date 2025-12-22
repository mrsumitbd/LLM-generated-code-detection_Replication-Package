from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class MeetingInfo:
    """Meeting information extracted from calendar events."""

    start: datetime
    end: datetime
    attendees: Optional[List[str]] = field(default_factory=list)

    def __post_init__(self):
        if self.end <= self.start:
            raise ValueError("Meeting end time must be after start time.")
        if self.attendees is None:
            self.attendees = []

    @property
    def duration_minutes(self) -> int:
        """Return the meeting duration in whole minutes."""
        delta = self.end - self.start
        return int(delta.total_seconds() // 60)

    @property
    def attendee_count(self) -> int:
        """Return the number of attendees."""
        return len(self.attendees)

    @property
    def display_attendees(self) -> str:
        """Return a comma‑separated string of attendee names."""
        return ", ".join(self.attendees)