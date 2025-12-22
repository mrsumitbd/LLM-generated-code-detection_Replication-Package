from typing import Dict
from datetime import datetime, timedelta
import threading

class UserSession:
    def __init__(self, user_id: str, timeout: int):
        self.user_id = user_id
        self.timeout = timeout
        self.created_at = datetime.now()
        self.last_accessed = datetime.now()
        self.data = {}
    
    def is_expired(self) -> bool:
        return datetime.now() - self.last_accessed > timedelta(seconds=self.timeout)
    
    def access(self):
        self.last_accessed = datetime.now()
    
    def set(self, key: str, value):
        self.data[key] = value
    
    def get(self, key: str):
        return self.data.get(key)

class SessionManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(SessionManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, session_timeout=300):
        if not hasattr(self, '_initialized'):
            self.session_timeout = session_timeout
            self.sessions: Dict[str, UserSession] = {}
            self._lock = threading.Lock()
            self._initialized = True

    def get_session(self, user_id: str) -> UserSession:
        with self._lock:
            if user_id not in self.sessions:
                self.sessions[user_id] = UserSession(user_id, self.session_timeout)
            else:
                session = self.sessions[user_id]
                if session.is_expired():
                    self.sessions[user_id] = UserSession(user_id, self.session_timeout)
                else:
                    session.access()
            
            return self.sessions[user_id]

    def cleanup(self):
        with self._lock:
            expired_users = [
                user_id for user_id, session in self.sessions.items()
                if session.is_expired()
            ]
            for user_id in expired_users:
                del self.sessions[user_id]