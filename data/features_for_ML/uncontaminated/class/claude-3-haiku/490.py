import signal
import threading

class ExecutionController:
    """
    Manages execution state and provides global Ctrl+C (SIGINT) handler functionality.
    
    Handles:
    - Single Ctrl+C: Cancels current operation
    - Double Ctrl+C: Exits Katalyst completely
    """

    def __init__(self):
        self._is_cancelled = False
        self._double_ctrl_c_lock = threading.Lock()
        self._original_sigint_handler = None

    def is_cancelled(self) -> bool:
        return self._is_cancelled

    def cancel(self):
        self._is_cancelled = True

    def reset(self):
        self._is_cancelled = False

    def check_cancelled(self, context: str = ""):
        if self.is_cancelled():
            raise KeyboardInterrupt(f"Operation cancelled{f' ({context})' if context else ''}")

    def setup_signal_handlers(self):
        self._original_sigint_handler = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, self._handle_sigint)

    def restore_signal_handlers(self):
        signal.signal(signal.SIGINT, self._original_sigint_handler)

    def _handle_sigint(self, signum, frame):
        with self._double_ctrl_c_lock:
            if self._is_cancelled:
                self._original_sigint_handler(signum, frame)
            else:
                self.cancel()
                print("\nOperation cancelled. Press Ctrl+C again to exit.")

    def wrap_execution(self, func: Callable, *args, **kwargs):
        try:
            self.setup_signal_handlers()
            return func(*args, **kwargs)
        finally:
            self.restore_signal_handlers()