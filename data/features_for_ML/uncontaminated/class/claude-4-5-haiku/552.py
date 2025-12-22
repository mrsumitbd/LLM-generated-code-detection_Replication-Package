import os
import sys
import readline
import atexit
from pathlib import Path


class CliApp:

    def __init__(self):
        self.history_file = os.path.expanduser("~/.cli_app_history")
        self.commands = []
        self.setup_readline()
        self._print_welcome_message()

    def _handle_keyboard_interrupt(self):
        print("\n\nKeyboardInterrupt: Exiting application.")
        sys.exit(0)

    def _handle_error(self, error):
        print(f"Error: {error}", file=sys.stderr)

    def _print_welcome_message(self):
        print("Welcome to CLI App")
        print("Type 'help' for available commands or 'exit' to quit.")

    def setup_readline(self):
        if os.path.exists(self.history_file):
            readline.read_history_file(self.history_file)
        
        readline.set_completer(self.completer)
        readline.parse_and_bind("tab: complete")
        atexit.register(self.save_history, None)

    def completer(self, text, state):
        if state == 0:
            self.commands = [cmd for cmd in self._get_available_commands() if cmd.startswith(text)]
        
        if state < len(self.commands):
            return self.commands[state]
        return None

    def save_history(self, input_text):
        try:
            readline.write_history_file(self.history_file)
        except Exception as e:
            self._handle_error(f"Failed to save history: {e}")

    def _get_available_commands(self):
        return ["help", "exit", "status", "info", "clear"]