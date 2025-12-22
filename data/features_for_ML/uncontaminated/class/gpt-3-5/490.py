import signal
import sys
from typing import Callable

class ExecutionController:
    def __init__(self):
        self.cancelled = False
        self.setup_signal_handlers()

    def is_cancelled(self) -> bool:
        return self.cancelled

    def cancel(self):
        self.cancelled = True

    def reset(self):
        self.cancelled = False

    def check_cancelled(self, context: str = ""):
        if self.is_cancelled():
            print(f"Cancelled operation: {context}")
            sys.exit(1)

    def setup_signal_handlers(self):
        signal.signal(signal.SIGINT, self._signal_handler)

    def restore_signal_handlers(self):
        signal.signal(signal.SIGINT, signal.default_int_handler)

    def wrap_execution(self, func: Callable, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            self.cancel()
            print("\nOperation cancelled.")
            sys.exit(1)

    def _signal_handler(self, signum, frame):
        if self.is_cancelled():
            print("\nExiting Katalyst completely.")
            sys.exit(1)
        else:
            print("\nOperation cancelled.")
            self.cancel()