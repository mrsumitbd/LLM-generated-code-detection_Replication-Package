class Session:

    def __init__(self, session_data: Dict[str, Any] = None):
        if session_data is None:
            session_data = {}
        
        self.id = session_data.get('id', '')
        self.name = session_data.get('name', '')
        self.host = session_data.get('host', '')
        self.port = session_data.get('port', 22)
        self.username = session_data.get('username', '')
        self.password = session_data.get('password', '')
        self.commands = session_data.get('commands', [])
        self.console_content = session_data.get('console_content', '')
        self.host_key = session_data.get('host_key', '')
        self.processes_md5 = session_data.get('processes_md5', '')
        self.created_at = session_data.get('created_at', '')
        self.updated_at = session_data.get('updated_at', '')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'host': self.host,
            'port': self.port,
            'username': self.username,
            'password': self.password,
            'commands': self.commands,
            'console_content': self.console_content,
            'host_key': self.host_key,
            'processes_md5': self.processes_md5,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def save(self, session_manager: 'SessionManager'):
        session_manager.save_session(self)

    def add_command(self, command: str):
        if command not in self.commands:
            self.commands.append(command)

    def update_console(self, content: str):
        self.console_content += content

    def set_host_key(self, host_key: str, session_manager):
        self.host_key = host_key
        self.save(session_manager)

    def set_processes_md5(self, md5: str, session_manager):
        self.processes_md5 = md5
        self.save(session_manager)