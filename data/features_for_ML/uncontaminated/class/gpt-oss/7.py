import uuid
import time
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any


@dataclass
class Session:
    session_id: str
    claude_wrapper: Any
    rows: int
    cols: int
    last_accessed: float


class SessionManager:
    """Manages persistent sessions across reconnections"""

    def __init__(self, session_timeout: int = 3600):
        """
        Initialize the session manager.

        :param session_timeout: Time in seconds after which a session is considered expired.
        """
        self._session_timeout = session_timeout
        self._sessions: Dict[str, Session] = {}

    def _cleanup_expired(self) -> None:
        """Remove expired sessions."""
        now = time.time()
        expired = [
            sid for sid, sess in self._sessions.items()
            if now - sess.last_accessed > self._session_timeout
        ]
        for sid in expired:
            del self._sessions[sid]

    def create_session(self, claude_wrapper, rows: int = 24, cols: int = 80) -> str:
        """
        Create a new session and return its ID.

        :param claude_wrapper: The wrapper object to associate with the session.
        :param rows: Number of rows for the session.
        :param cols: Number of columns for the session.
        :return: The generated session ID.
        """
        self._cleanup_expired()
        session_id = str(uuid.uuid4())
        session = Session(
            session_id=session_id,
            claude_wrapper=claude_wrapper,
            rows=rows,
            cols=cols,
            last_accessed=time.time(),
        )
        self._sessions[session_id] = session
        return session_id

    def get_session(self, session_id: str) -> Optional[Session]:
        """
        Retrieve a session by its ID.

        :param session_id: The ID of the session to retrieve.
        :return: The Session object or None if not found or expired.
        """
        self._cleanup_expired()
        session = self._sessions.get(session_id)
        if session:
            session.last_accessed = time.time()
        return session

    def destroy_session(self, session_id: str) -> None:
        """
        Destroy a session by its ID.

        :param session_id: The ID of the session to destroy.
        """
        self._sessions.pop(session_id, None)

    def list_sessions(self) -> Dict[str, dict]:
        """
        List all active sessions.

        :return: A dictionary mapping session IDs to session metadata.
        """
        self._cleanup_expired()
        return {
            sid: {
                "rows": sess.rows,
                "cols": sess.cols,
                "last_accessed": sess.last_accessed,
            }
            for sid, sess in self._sessions.items()
        }

    def get_session_count(self) -> int:
        """
        Get the number of active sessions.

        :return: The count of active sessions.
        """
        self._cleanup_expired()
        return len(self._sessions)