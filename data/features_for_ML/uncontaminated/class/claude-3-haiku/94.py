import time
from typing import Dict

class UserSession:
    def __init__(self, user_id: str, created_at: float):
        self.user_id = user_id
        self.created_at = created_at

class SessionManager:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(SessionManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, session_timeout=300):
        self.session_timeout = session_timeout
        self.sessions: Dict[str, UserSession] = {}

    def get_session(self, user_id: str) -> UserSession:
        if user_id in self.sessions:
            session = self.sessions[user_id]
            if time.time() - session.created_at <= self.session_timeout:
                return session
            else:
                del self.sessions[user_id]
        session = UserSession(user_id, time.time())
        self.sessions[user_id] = session
        return session

    def cleanup(self):
        current_time = time.time()
        for user_id, session in list(self.sessions.items()):
            if current_time - session.created_at > self.session_timeout:
                del self.sessions[user_id]