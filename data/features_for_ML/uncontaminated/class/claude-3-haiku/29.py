class SessionManager:
    """Manages HTTP sessions with authentication"""

    def __init__(self, config: FOClientConfig, auth_manager: AuthenticationManager):
        self.config = config
        self.auth_manager = auth_manager
        self.sessions = {}

    def create_session(self, user_id: str) -> str:
        session_id = self._generate_session_id(user_id)
        self.sessions[session_id] = {
            "user_id": user_id,
            "expiration_time": time.time() + self.config.session_duration
        }
        return session_id

    def _generate_session_id(self, user_id: str) -> str:
        return f"{user_id}_{uuid.uuid4().hex}"

    def validate_session(self, session_id: str) -> bool:
        if session_id not in self.sessions:
            return False

        session_data = self.sessions[session_id]
        if session_data["expiration_time"] < time.time():
            del self.sessions[session_id]
            return False

        return True

    def authenticate_user(self, username: str, password: str) -> str:
        user_id = self.auth_manager.authenticate_user(username, password)
        if user_id:
            return self.create_session(user_id)
        else:
            return ""

    def logout_user(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]