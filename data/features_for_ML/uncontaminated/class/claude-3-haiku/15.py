class CachedMeeting:
    """Cached meeting information with expiration."""

    def __init__(self, meeting_id, start_time, end_time, participants):
        self.meeting_id = meeting_id
        self.start_time = start_time
        self.end_time = end_time
        self.participants = participants
        self.expiration_time = None

    def set_expiration(self, expiration_time):
        self.expiration_time = expiration_time

    def is_expired(self):
        if self.expiration_time is None:
            return False
        return self.expiration_time < datetime.now()

    def __str__(self):
        return f"Meeting ID: {self.meeting_id}, Start: {self.start_time}, End: {self.end_time}, Participants: {self.participants}"