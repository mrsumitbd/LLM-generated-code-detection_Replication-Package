class App:
    def __init__(self, manager: StreamableHTTPSessionManager) -> None:
        self.manager = manager
        self.sessions = {}

    def create_session(self, user_id: str) -> HTTPSession:
        if user_id in self.sessions:
            return self.sessions[user_id]
        else:
            session = self.manager.create_session(user_id)
            self.sessions[user_id] = session
            return session

    def delete_session(self, user_id: str) -> None:
        if user_id in self.sessions:
            self.manager.delete_session(self.sessions[user_id])
            del self.sessions[user_id]

    def get_session(self, user_id: str) -> HTTPSession:
        if user_id in self.sessions:
            return self.sessions[user_id]
        else:
            raise ValueError(f"No session found for user_id: {user_id}")

    def stream_content(self, user_id: str, content: bytes) -> None:
        session = self.get_session(user_id)
        session.stream_content(content)