from typing import Dict
from datetime import datetime
import threading

class SessionManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SessionManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, session_timeout=300):
        if not hasattr(self, 'initialized'):
            self.sessions: Dict[str, UserSession] = {}
            self.timeout = session_timeout
            self.initialized = True
            self._lock = threading.Lock()

    def get_session(self, user_id: str) -> UserSession:
        self.cleanup()
        if user_id not in self.sessions:
            with self._lock:
                self.sessions[user_id] = UserSession(user_id)
        return self.sessions[user_id]

    def cleanup(self):
        expired = [
            uid for uid, session in self.sessions.items()
            if (datetime.now() - session.last_active).seconds > self.timeout
        ]
        for uid in expired:
            with self._lock:
                del self.sessions[uid]