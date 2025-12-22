import os
import sys
import readline
import atexit

class CliApp:
    def __init__(self):
        # Basic command list for completion
        self.commands = [
            'help', 'exit', 'quit', 'list', 'show',
            'add', 'remove', 'update', 'search', 'clear'
        ]
        # History file in the user's home directory
        self.history_file = os.path.expanduser('~/.cliapp_history')
        self.setup_readline()
        self._print_welcome_message()

    def _handle_keyboard_interrupt(self):
        """Handle Ctrl+C gracefully."""
        print('\nKeyboardInterrupt received. Exiting.')
        sys.exit(0)

    def _handle_error(self, error):
        """Print an error message."""
        print(f'Error: {error}', file=sys.stderr)

    def _print_welcome_message(self):
        """Display a welcome banner."""
        banner = (
            "=====================================\n"
            "          Welcome to CliApp          \n"
            "=====================================\n"
            "Type 'help' to see available commands.\n"
        )
        print(banner)

    def setup_readline(self):
        """Configure readline for history and completion."""
        # Set the completer function
        readline.set_completer(self.completer)
        # Use tab for completion
        readline.parse_and_bind('tab: complete')
        # Load history if it exists
        if os.path.exists(self.history_file):
            try:
                readline.read_history_file(self.history_file)
            except Exception as e:
                self._handle_error(f'Could not read history file: {e}')
        # Ensure history is saved on exit
        atexit.register(self.save_history, None)

    def completer(self, text, state):
        """Return the next possible completion for 'text'."""
        options = [cmd for cmd in self.commands if cmd.startswith(text)]
        if state < len(options):
            return options[state]
        else:
            return None

    def save_history(self, input_text):
        """Write the readline history to the history file."""
        try:
            readline.write_history_file(self.history_file)
        except Exception as e:
            self._handle_error(f'Could not write history file: {e}')