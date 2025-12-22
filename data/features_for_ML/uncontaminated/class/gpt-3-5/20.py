from typing import Dict, Any

class Session:

    def __init__(self, session_data: Dict[str, Any] = None):
        self.session_data = session_data if session_data is not None else {}

    def to_dict(self) -> Dict[str, Any]:
        return self.session_data

    def save(self, session_manager: 'SessionManager'):
        session_manager.save_session(self)

    def add_command(self, command: str):
        self.session_data.setdefault('commands', []).append(command)

    def update_console(self, content: str):
        self.session_data['console'] = content

    def set_host_key(self, host_key: str, session_manager):
        self.session_data['host_key'] = host_key
        session_manager.save_session(self)

    def set_processes_md5(self, md5: str, session_manager):
        self.session_data['processes_md5'] = md5
        session_manager.save_session(self)