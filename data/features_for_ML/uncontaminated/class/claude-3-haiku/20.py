class Session:
    def __init__(self, session_data: Dict[str, Any] = None):
        if session_data:
            self.__dict__.update(session_data)
        else:
            self.commands = []
            self.console_content = ""
            self.host_key = ""
            self.processes_md5 = ""

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__

    def save(self, session_manager: 'SessionManager'):
        session_manager.save_session(self)

    def add_command(self, command: str):
        self.commands.append(command)

    def update_console(self, content: str):
        self.console_content = content

    def set_host_key(self, host_key: str, session_manager):
        self.host_key = host_key
        session_manager.update_host_key(self)

    def set_processes_md5(self, md5: str, session_manager):
        self.processes_md5 = md5
        session_manager.update_processes_md5(self)