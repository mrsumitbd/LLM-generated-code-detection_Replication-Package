class CommandHandler:
    """Manage command registration and execution"""

    def __init__(self, app: Any):
        self.app = app
        self.commands: Dict[str, Callable] = {}
        self._register_core_commands()
        self._register_debug_commands()

    def _register_core_commands(self) -> None:
        """Register core commands"""
        self.register_command("help", self._handle_help)
        self.register_command("exit", self._handle_exit)
        self.register_command("quit", self._handle_exit)

    def _register_debug_commands(self) -> None:
        """Register debug commands"""
        self.register_command("debug", self._handle_debug)
        self.register_command("status", self._handle_status)

    def register_command(self, command: str, handler: Callable) -> None:
        """Register a command with its handler"""
        if not isinstance(command, str) or not command.strip():
            raise ValueError("Command must be a non-empty string")
        if not callable(handler):
            raise TypeError("Handler must be callable")
        self.commands[command.lower()] = handler

    def deregister_command(self, command: str) -> None:
        """Deregister a command"""
        command_lower = command.lower()
        if command_lower in self.commands:
            del self.commands[command_lower]

    def get_commands(self) -> Dict[str, Callable]:
        """Get all registered commands"""
        return self.commands.copy()

    def _handle_help(self) -> str:
        """Handle help command"""
        commands_list = ", ".join(sorted(self.commands.keys()))
        return f"Available commands: {commands_list}"

    def _handle_exit(self) -> None:
        """Handle exit/quit command"""
        if hasattr(self.app, 'exit'):
            self.app.exit()

    def _handle_debug(self) -> str:
        """Handle debug command"""
        return "Debug mode enabled"

    def _handle_status(self) -> str:
        """Handle status command"""
        return f"Status: {len(self.commands)} commands registered"