from typing import Any, Callable, Dict

class CommandHandler:
    """Manage command registration and execution"""

    def __init__(self, app: Any):
        self.app = app
        self.commands = {}

        self._register_core_commands()
        self._register_debug_commands()

    def _register_core_commands(self) -> None:
        self.register_command('help', self._handle_help)
        self.register_command('quit', self._handle_quit)

    def _register_debug_commands(self) -> None:
        self.register_command('debug', self._handle_debug)

    def register_command(self, command: str, handler: Callable) -> None:
        self.commands[command] = handler

    def deregister_command(self, command: str) -> None:
        if command in self.commands:
            del self.commands[command]

    def get_commands(self) -> Dict[str, Callable]:
        return self.commands

    def _handle_help(self):
        print("Help command executed")

    def _handle_quit(self):
        print("Quit command executed")

    def _handle_debug(self):
        print("Debug command executed")

# Example usage
def main():
    handler = CommandHandler("my_app")
    commands = handler.get_commands()
    print(commands)

if __name__ == "__main__":
    main()