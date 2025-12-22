class SessionData:
    def __init__(self, session_id, start_time, end_time, commands):
        self.session_id = session_id
        self.start_time = start_time
        self.end_time = end_time
        self.commands = commands

    def get_session_id(self):
        return self.session_id

    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time

    def get_commands(self):
        return self.commands

    def set_session_id(self, session_id):
        self.session_id = session_id

    def set_start_time(self, start_time):
        self.start_time = start_time

    def set_end_time(self, end_time):
        self.end_time = end_time

    def set_commands(self, commands):
        self.commands = commands

# Example usage:
# session = SessionData(1, "2022-01-01 10:00:00", "2022-01-01 11:00:00", ["ls", "cd", "mkdir"])
# print(session.get_session_id())
# print(session.get_start_time())
# print(session.get_end_time())
# print(session.get_commands())