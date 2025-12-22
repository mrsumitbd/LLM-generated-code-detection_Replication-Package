import signal
import sys
from typing import Callable
from datetime import datetime, timedelta


class ExecutionController:
    """
    Manages execution state and provides global Ctrl+C (SIGINT) handler functionality.
    
    Handles:
    - Single Ctrl+C: Cancels current operation
    - Double Ctrl+C: Exits Katalyst completely
    """

    def __init__(self):
        self._cancelled = False
        self._original_sigint_handler = None
        self._last_sigint_time = None
        self._sigint_count = 0
        self._double_sigint_threshold = 0.5  # seconds

    def is_cancelled(self) -> bool:
        return self._cancelled

    def cancel(self):
        self._cancelled = True

    def reset(self):
        self._cancelled = False
        self._sigint_count = 0
        self._last_sigint_time = None

    def check_cancelled(self, context: str = ""):
        if self._cancelled:
            message = f"Execution cancelled"
            if context:
                message += f" ({context})"
            raise KeyboardInterrupt(message)

    def setup_signal_handlers(self):
        self._original_sigint_handler = signal.signal(signal.SIGINT, self._handle_sigint)

    def restore_signal_handlers(self):
        if self._original_sigint_handler is not None:
            signal.signal(signal.SIGINT, self._original_sigint_handler)
            self._original_sigint_handler = None

    def _handle_sigint(self, signum, frame):
        current_time = datetime.now()
        
        # Check if this is a double Ctrl+C within threshold
        if self._last_sigint_time is not None:
            time_diff = (current_time - self._last_sigint_time).total_seconds()
            if time_diff < self._double_sigint_threshold:
                self._sigint_count += 1
                if self._sigint_count >= 2:
                    # Double Ctrl+C: Exit completely
                    self.restore_signal_handlers()
                    sys.exit(1)
            else:
                # Reset counter if threshold exceeded
                self._sigint_count = 1
        else:
            self._sigint_count = 1
        
        self._last_sigint_time = current_time
        
        # Single Ctrl+C: Cancel current operation
        self.cancel()

    def wrap_execution(self, func: Callable, *args, **kwargs):
        try:
            self.setup_signal_handlers()
            self.reset()
            result = func(*args, **kwargs)
            return result
        finally:
            self.restore_signal_handlers()
            self.reset()