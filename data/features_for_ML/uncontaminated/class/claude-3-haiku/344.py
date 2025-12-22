from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

@dataclass
class MeetingInfo:
    """Meeting information extracted from calendar events."""
    start_time: datetime
    end_time: datetime
    attendees: List[str]

    def __post_init__(self):
        if self.start_time >= self.end_time:
            raise ValueError("Start time must be before end time.")

    @property
    def duration_minutes(self) -> int:
        return int((self.end_time - self.start_time).total_seconds() // 60)

    @property
    def attendee_count(self) -> int:
        return len(self.attendees)

    @property
    def display_attendees(self) -> str:
        return ", ".join(self.attendees)