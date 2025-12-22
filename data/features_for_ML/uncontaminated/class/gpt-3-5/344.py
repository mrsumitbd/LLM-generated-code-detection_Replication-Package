class MeetingInfo:
    """Meeting information extracted from calendar events."""

    def __init__(self, start_time: str, end_time: str, attendees: list):
        self.start_time = start_time
        self.end_time = end_time
        self.attendees = attendees

    @property
    def duration_minutes(self) -> int:
        start = datetime.datetime.strptime(self.start_time, '%H:%M')
        end = datetime.datetime.strptime(self.end_time, '%H:%M')
        duration = end - start
        return duration.total_seconds() // 60

    @property
    def attendee_count(self) -> int:
        return len(self.attendees)

    @property
    def display_attendees(self) -> str:
        return ', '.join(self.attendees)