import time

class CachedMeeting:
    """Cached meeting information with expiration."""

    def __init__(self, meeting_info, expiration_time):
        self.meeting_info = meeting_info
        self.expiration_time = time.time() + expiration_time

    def is_valid(self):
        return time.time() < self.expiration_time

    def get_meeting_info(self):
        if self.is_valid():
            return self.meeting_info
        else:
            return None