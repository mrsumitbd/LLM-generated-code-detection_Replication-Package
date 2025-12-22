import time
from typing import Optional, Dict

class Session:
    def __init__(self, session_id: str, claude_wrapper, rows: int, cols: int):
        self.session_id = session_id
        self.claude_wrapper = claude_wrapper
        self.rows = rows
        self.cols = cols
        self.last_activity = time.time()

class SessionManager:
    """Manages persistent sessions across reconnections"""

    def __init__(self, session_timeout: int = 3600):
        self.sessions = {}
        self.session_timeout = session_timeout

    def create_session(self, claude_wrapper, rows: int = 24, cols: int = 80) -> str:
        session_id = f"session_{len(self.sessions) + 1}"
        session = Session(session_id, claude_wrapper, rows, cols)
        self.sessions[session_id] = session
        return session_id

    def get_session(self, session_id: str) -> Optional[Session]:
        if session_id in self.sessions:
            session = self.sessions[session_id]
            if time.time() - session.last_activity <= self.session_timeout:
                session.last_activity = time.time()
                return session
            else:
                self.destroy_session(session_id)
        return None

    def destroy_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]

    def list_sessions(self) -> Dict[str, dict]:
        return {session_id: {"rows": session.rows, "cols": session.cols} for session_id, session in self.sessions.items()}

    def get_session_count(self) -> int:
        return len(self.sessions)