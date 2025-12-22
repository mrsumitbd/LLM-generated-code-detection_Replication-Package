class SessionManager:
    """Manages persistent sessions across reconnections"""

    def __init__(self, session_timeout: int = 3600):
        self.session_timeout = session_timeout
        self.sessions: Dict[str, Session] = {}
        self.session_timestamps: Dict[str, float] = {}

    def create_session(self, claude_wrapper, rows: int = 24, cols: int = 80) -> str:
        import uuid
        import time
        
        session_id = str(uuid.uuid4())
        session = Session(session_id, claude_wrapper, rows, cols)
        self.sessions[session_id] = session
        self.session_timestamps[session_id] = time.time()
        return session_id

    def get_session(self, session_id: str) -> Optional[Session]:
        import time
        
        if session_id not in self.sessions:
            return None
        
        current_time = time.time()
        session_time = self.session_timestamps.get(session_id, current_time)
        
        if current_time - session_time > self.session_timeout:
            self.destroy_session(session_id)
            return None
        
        self.session_timestamps[session_id] = current_time
        return self.sessions[session_id]

    def destroy_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]
        if session_id in self.session_timestamps:
            del self.session_timestamps[session_id]

    def list_sessions(self) -> Dict[str, dict]:
        import time
        
        current_time = time.time()
        active_sessions = {}
        
        expired_sessions = []
        for session_id, session_time in self.session_timestamps.items():
            if current_time - session_time > self.session_timeout:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            self.destroy_session(session_id)
        
        for session_id, session in self.sessions.items():
            if session_id in self.session_timestamps:
                active_sessions[session_id] = {
                    "created": self.session_timestamps[session_id],
                    "rows": session.rows,
                    "cols": session.cols,
                    "history_length": len(session.history) if hasattr(session, 'history') else 0
                }
        
        return active_sessions

    def get_session_count(self) -> int:
        import time
        
        current_time = time.time()
        expired_sessions = []
        
        for session_id, session_time in self.session_timestamps.items():
            if current_time - session_time > self.session_timeout:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            self.destroy_session(session_id)
        
        return len(self.sessions)