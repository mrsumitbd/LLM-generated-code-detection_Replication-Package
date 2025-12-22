from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class MeetingInfo:
    """Meeting information extracted from calendar events."""
    
    title: str
    start_time: datetime
    end_time: datetime
    attendees: List[str]
    location: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        if not self.attendees:
            raise ValueError("attendees list cannot be empty")

    @property
    def duration_minutes(self) -> int:
        delta = self.end_time - self.start_time
        return int(delta.total_seconds() / 60)

    @property
    def attendee_count(self) -> int:
        return len(self.attendees)

    @property
    def display_attendees(self) -> str:
        if not self.attendees:
            return ""
        if len(self.attendees) == 1:
            return self.attendees[0]
        if len(self.attendees) == 2:
            return f"{self.attendees[0]} and {self.attendees[1]}"
        return f"{', '.join(self.attendees[:-1])} and {self.attendees[-1]}"