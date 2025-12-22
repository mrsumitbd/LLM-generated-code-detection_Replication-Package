from typing import Any, Callable, Dict


class CommandHandler:
    """Manage command registration and execution"""

    def __init__(self, app: Any):
        self.app = app
        self._commands: Dict[str, Callable] = {}
        self._register_core_commands()
        self._register_debug_commands()

    def _register_core_commands(self) -> None:
        """Register built‑in commands that are always available."""
        self.register_command("help", self._cmd_help)
        self.register_command("exit", self._cmd_exit)
        self.register_command("status", self._cmd_status)

    def _register_debug_commands(self) -> None:
        """Register debug‑only commands."""
        self.register_command("debug", self._cmd_debug)
        self.register_command("log", self._cmd_log)

    def register_command(self, command: str, handler: Callable) -> None:
        """Add a command to the registry."""
        if command in self._commands:
            raise ValueError(f"Command '{command}' is already registered.")
        self._commands[command] = handler

    def deregister_command(self, command: str) -> None:
        """Remove a command from the registry."""
        if command not in self._commands:
            raise KeyError(f"Command '{command}' is not registered.")
        del self._commands[command]

    def get_commands(self) -> Dict[str, Callable]:
        """Return a copy of the registered commands."""
        return dict(self._commands)

    # ------------------------------------------------------------------
    # Core command implementations
    # ------------------------------------------------------------------
    def _cmd_help(self, *args: Any) -> None:
        """Print a list of available commands."""
        print("Available commands:")
        for cmd in sorted(self._commands):
            print(f"  {cmd}")

    def _cmd_exit(self, *args: Any) -> None:
        """Exit the application."""
        print("Exiting...")
        if hasattr(self.app, "shutdown"):
            self.app.shutdown()
        else:
            import sys
            sys.exit(0)

    def _cmd_status(self, *args: Any) -> None:
        """Print a simple status message."""
        print("Application status: running")

    # ------------------------------------------------------------------
    # Debug command implementations
    # ------------------------------------------------------------------
    def _cmd_debug(self, *args: Any) -> None:
        """Print debug information about the app."""
        print("Debug info:")
        if hasattr(self.app, "__dict__"):
            for k, v in self.app.__dict__.items():
                print(f"  {k} = {v!r}")
        else:
            print("  No debug info available.")

    def _cmd_log(self, *args: Any) -> None:
        """Log a message to the app's logger if available."""
        message = " ".join(map(str, args)) if args else "No message"
        if hasattr(self.app, "logger"):
            self.app.logger.info(f"LOG: {message}")
        else:
            print(f"LOG: {message}")