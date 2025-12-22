from datetime import datetime
from typing import Dict, Any, List

class Session:
    def __init__(self, session_data: Dict[str, Any] = None):
        default_values = {
            'id': f"session_{datetime.now().timestamp()}",
            'name': 'New Session',
            'host': 'localhost',
            'username': 'user',
            'port': 22,
            'auth_type': 'password',
            'password': '',
            'key_path': '',
            'status': 'disconnected',
            'created_at': datetime.now().isoformat(),
            'history': [],
            'console_content': '',
            'host_key': '',
            'processes_md5': '',
            'proxy_type': 'None',
            'proxy_host': '',
            'proxy_port': 0,
            'proxy_username': '',
            'proxy_password': '',
            "ssh_default_path": "",
            "file_manager_default_path": "",
            "jump_server": ""
        }
        if session_data:
            for key, default_value in default_values.items():
                setattr(self, key, session_data.get(key, default_value))
        else:
            for key, value in default_values.items():
                setattr(self, key, value)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'host': self.host,
            'username': self.username,
            'port': self.port,
            'auth_type': self.auth_type,
            'password': self.password,
            'key_path': self.key_path,
            'status': self.status,
            'created_at': self.created_at,
            'history': self.history,
            'console_content': self.console_content,
            'host_key': self.host_key,
            'processes_md5': self.processes_md5,
            'proxy_type': self.proxy_type,
            'proxy_host': self.proxy_host,
            'proxy_port': self.proxy_port,
            'proxy_username': self.proxy_username,
            'proxy_password': self.proxy_password,
            "ssh_default_path": self.ssh_default_path,
            "file_manager_default_path": self.file_manager_default_path,
            "jump_server": self.jump_server
        }

    def save(self, session_manager: 'SessionManager'):
        sessions = session_manager.sessions_cache
        for i, session in enumerate(sessions):
            if session.id == self.id:
                sessions[i] = self
                break
        else:
            sessions.append(self)
        session_manager.save_sessions(sessions)

    def add_command(self, command: str):
        if command.strip() and command not in self.history:
            self.history.append(command)
            if len(self.history) > 30:
                self.history.pop(0)

    def update_console(self, content: str):
        self.console_content = content

    def set_host_key(self, host_key: str, session_manager):
        self.host_key = host_key

    def set_processes_md5(self, md5: str, session_manager):
        self.processes_md5 = md5
        session_manager.save_sessions(session_manager.sessions_cache)