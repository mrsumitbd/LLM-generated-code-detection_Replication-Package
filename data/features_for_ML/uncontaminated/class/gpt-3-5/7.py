from typing import Optional, Dict

class SessionManager:
    """Manages persistent sessions across reconnections"""

    def __init__(self, session_timeout: int = 3600):
        self.session_timeout = session_timeout
        self.sessions = {}

    def create_session(self, claude_wrapper, rows: int = 24, cols: int = 80) -> str:
        session_id = str(hash(claude_wrapper))
        self.sessions[session_id] = {
            'claude_wrapper': claude_wrapper,
            'rows': rows,
            'cols': cols
        }
        return session_id

    def get_session(self, session_id: str) -> Optional[dict]:
        return self.sessions.get(session_id)

    def destroy_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]

    def list_sessions(self) -> Dict[str, dict]:
        return self.sessions

    def get_session_count(self) -> int:
        return len(self.sessions)