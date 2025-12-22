class EventCfg:
    """Configuration for events."""

    def __init__(self, name, start_time, end_time, location, description):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
        self.description = description

    def __str__(self):
        return f"{self.name} - {self.start_time} to {self.end_time} at {self.location}"

    def __repr__(self):
        return f"EventCfg('{self.name}', '{self.start_time}', '{self.end_time}', '{self.location}', '{self.description}')"

    def is_overlapping(self, other):
        """Check if the event overlaps with another event."""
        return (
            self.start_time <= other.end_time
            and other.start_time <= self.end_time
        )

    def is_on_same_day(self, other):
        """Check if the event is on the same day as another event."""
        return self.start_time.date() == other.start_time.date()