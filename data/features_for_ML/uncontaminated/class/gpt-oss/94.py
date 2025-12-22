import datetime
import threading
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class UserSession:
    """Represents a user session."""
    user_id: str
    created_at: datetime.datetime
    last_accessed: datetime.datetime

    def touch(self) -> None:
        """Update the last accessed time to now."""
        self.last_accessed = datetime.datetime.utcnow()


class SessionManager:
    """Singleton manager for user sessions with timeout support."""

    _instance: Optional["SessionManager"] = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(SessionManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, session_timeout: int = 300):
        # Avoid reinitializing on subsequent calls
        if hasattr(self, "_initialized") and self._initialized:
            return
        self.session_timeout = datetime.timedelta(seconds=session_timeout)
        self._sessions: Dict[str, UserSession] = {}
        self._sessions_lock = threading.Lock()
        self._initialized = True

    def get_session(self, user_id: str) -> UserSession:
        """Return an existing session or create a new one."""
        now = datetime.datetime.utcnow()
        with self._sessions_lock:
            session = self._sessions.get(user_id)
            if session is None:
                session = UserSession(
                    user_id=user_id,
                    created_at=now,
                    last_accessed=now,
                )
                self._sessions[user_id] = session
            else:
                session.touch()
            return session

    def cleanup(self) -> None:
        """Remove sessions that have expired."""
        now = datetime.datetime.utcnow()
        with self._sessions_lock:
            expired = [
                uid
                for uid, sess in self._sessions.items()
                if now - sess.last_accessed > self.session_timeout
            ]
            for uid in expired:
                del self._sessions[uid]