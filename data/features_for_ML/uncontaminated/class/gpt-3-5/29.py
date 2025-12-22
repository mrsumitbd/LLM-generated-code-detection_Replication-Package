from typing import Any

class SessionManager:
    """Manages HTTP sessions with authentication"""

    def __init__(self, config: Any, auth_manager: Any):
        self.config = config
        self.auth_manager = auth_manager

    def start_session(self):
        print("Starting session...")

    def end_session(self):
        print("Ending session...")

    def send_request(self, url: str, data: dict):
        print(f"Sending request to {url} with data: {data}")

# Example usage:
class FOClientConfig:
    pass

class AuthenticationManager:
    pass

config = FOClientConfig()
auth_manager = AuthenticationManager()

session_manager = SessionManager(config, auth_manager)
session_manager.start_session()
session_manager.send_request("http://example.com/api", {"key": "value"})
session_manager.end_session()