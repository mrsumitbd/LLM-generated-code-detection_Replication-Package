from typing import List

class StreamableHTTPSessionManager:
    def __init__(self) -> None:
        self.sessions = []

    def add_session(self, session):
        self.sessions.append(session)

class App:
    def __init__(self, manager: StreamableHTTPSessionManager) -> None:
        self.manager = manager

# Example usage
manager = StreamableHTTPSessionManager()
app = App(manager)