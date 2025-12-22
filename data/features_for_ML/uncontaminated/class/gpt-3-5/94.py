class UserSession:
    def __init__(self, user_id):
        self.user_id = user_id

class SessionManager:
    _sessions = {}
    _session_timeout = 300

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(SessionManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, session_timeout=300):
        self._session_timeout = session_timeout

    def get_session(self, user_id: str) -> UserSession:
        if user_id in self._sessions:
            return self._sessions[user_id]
        else:
            new_session = UserSession(user_id)
            self._sessions[user_id] = new_session
            return new_session

    def cleanup(self):
        current_time = time.time()
        expired_sessions = [user_id for user_id, session in self._sessions.items() if current_time - session.last_accessed > self._session_timeout]
        for user_id in expired_sessions:
            del self._sessions[user_id]