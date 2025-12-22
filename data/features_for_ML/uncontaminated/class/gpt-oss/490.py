import signal
import sys
import time
from typing import Callable, Any


class ExecutionController:
    """
    Manages execution state and provides global Ctrl+C (SIGINT) handler functionality.

    Handles:
    - Single Ctrl+C: Cancels current operation
    - Double Ctrl+C: Exits Katalyst completely
    """

    def __init__(self):
        self._cancelled: bool = False
        self._original_handler = None
        self._last_sigint_time: float = 0.0
        self._double_sigint_threshold: float = 1.0  # seconds

    def is_cancelled(self) -> bool:
        return self._cancelled

    def cancel(self):
        self._cancelled = True

    def reset(self):
        self._cancelled = False

    def check_cancelled(self, context: str = ""):
        if self._cancelled:
            msg = f"Operation cancelled{': ' + context if context else ''}"
            raise RuntimeError(msg)

    def _handle_sigint(self, signum, frame):
        now = time.time()
        if now - self._last_sigint_time < self._double_sigint_threshold:
            # Double Ctrl+C: exit immediately
            sys.exit(0)
        self._last_sigint_time = now
        if not self._cancelled:
            self._cancelled = True
            # Optionally, inform the user
            print("\nCtrl+C pressed: cancelling current operation...")

    def setup_signal_handlers(self):
        self._original_handler = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, self._handle_sigint)

    def restore_signal_handlers(self):
        if self._original_handler is not None:
            signal.signal(signal.SIGINT, self._original_handler)
        else:
            signal.signal(signal.SIGINT, signal.SIG_DFL)

    def wrap_execution(self, func: Callable[..., Any], *args, **kwargs) -> Any:
        """
        Execute a function with global Ctrl+C handling.

        Parameters
        ----------
        func : Callable
            The function to execute.
        *args, **kwargs
            Arguments to pass to the function.

        Returns
        -------
        Any
            The result of the function call.
        """
        self.setup_signal_handlers()
        try:
            return func(*args, **kwargs)
        finally:
            self.restore_signal_handlers()