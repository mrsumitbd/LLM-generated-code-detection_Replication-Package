from typing import Any, Callable, Dict

class CommandHandler:
    """Manage command registration and execution"""

    def __init__(self, app: Any):
        self._app = app
        self._commands = {}
        self._register_core_commands()
        self._register_debug_commands()

    def _register_core_commands(self) -> None:
        self.register_command("help", self._handle_help)
        self.register_command("exit", self._handle_exit)

    def _register_debug_commands(self) -> None:
        self.register_command("debug_info", self._handle_debug_info)

    def register_command(self, command: str, handler: Callable) -> None:
        self._commands[command] = handler

    def deregister_command(self, command: str) -> None:
        if command in self._commands:
            del self._commands[command]

    def get_commands(self) -> Dict[str, Callable]:
        return self._commands.copy()

    def _handle_help(self, *args: Any) -> None:
        print("Available commands:")
        for cmd, handler in self._commands.items():
            print(f"- {cmd}")

    def _handle_exit(self, *args: Any) -> None:
        self._app.shutdown()

    def _handle_debug_info(self, *args: Any) -> None:
        print("Debug information:")
        # Add your debug information handling logic here