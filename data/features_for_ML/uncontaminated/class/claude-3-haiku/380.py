class SessionData:
    """Data entry for a terminal session."""

    def __init__(self, session_id, start_time, end_time, duration, commands):
        self.session_id = session_id
        self.start_time = start_time
        self.end_time = end_time
        self.duration = duration
        self.commands = commands

    def __str__(self):
        return f"Session ID: {self.session_id}, Start Time: {self.start_time}, End Time: {self.end_time}, Duration: {self.duration}, Commands: {self.commands}"

    def __repr__(self):
        return f"SessionData(session_id={self.session_id}, start_time='{self.start_time}', end_time='{self.end_time}', duration={self.duration}, commands={self.commands})"