import time
import threading
from typing import Callable, Optional


class RefreshTimer:
    """
    Manages automatic page refresh based on activity tracking.

    This class implements a two-stage timer system:
    1. Idle timeout: Wait for configured minutes of inactivity
    2. Grace period: Wait additional seconds before actually refreshing

    The timer resets whenever activity is detected.
    """

    def __init__(self,
                 idle_timeout_minutes: int = 5,
                 grace_period_seconds: int = 30,
                 check_interval_seconds: int = 1):
        """
        Initialize the RefreshTimer.

        :param idle_timeout_minutes: Minutes of inactivity before grace period starts.
        :param grace_period_seconds: Seconds to wait after grace period starts before refresh.
        :param check_interval_seconds: How often to poll the timer loop.
        """
        self.idle_timeout_minutes = self._apply_humanization(idle_timeout_minutes, 1)
        self.grace_period_seconds = self._apply_humanization(grace_period_seconds, 5)
        self.check_interval_seconds = max(check_interval_seconds, 1)

        self._refresh_callback: Optional[Callable] = None
        self._grace_start_callback: Optional[Callable] = None

        self._last_activity: float = time.time()
        self._in_grace: bool = False
        self._running: bool = False
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()

    def _apply_humanization(self, value: int, min_value: int) -> int:
        """
        Round up the value to the nearest multiple of min_value, ensuring it is at least min_value.
        """
        if value < min_value:
            return min_value
        return ((value + min_value - 1) // min_value) * min_value

    def start(self,
              refresh_callback: Callable,
              grace_period_start_callback: Optional[Callable] = None) -> None:
        """
        Start the timer loop.

        :param refresh_callback: Function to call when refresh should occur.
        :param grace_period_start_callback: Optional function to call when grace period starts.
        """
        with self._lock:
            if self._running:
                return
            self._refresh_callback = refresh_callback
            self._grace_start_callback = grace_period_start_callback
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._timer_loop, daemon=True)
            self._running = True
            self._thread.start()

    def stop(self) -> None:
        """
        Stop the timer loop.
        """
        with self._lock:
            if not self._running:
                return
            self._stop_event.set()
            if self._thread:
                self._thread.join()
            self._running = False
            self._in_grace = False

    def record_activity(self) -> None:
        """
        Record user activity, resetting the idle timer.
        """
        with self._lock:
            self._last_activity = time.time()
            self._in_grace = False

    def is_running(self) -> bool:
        """
        Return True if the timer loop is running.
        """
        with self._lock:
            return self._running

    def is_in_grace_period(self) -> bool:
        """
        Return True if currently in grace period.
        """
        with self._lock:
            return self._in_grace

    def get_time_until_next_check(self) -> float:
        """
        Return the time in seconds until the next check should occur.
        """
        with self._lock:
            now = time.time()
            if self._in_grace:
                elapsed = now - self._last_activity
                remaining = max(self.grace_period_seconds - elapsed, 0)
            else:
                elapsed = now - self._last_activity
                remaining = max(self.idle_timeout_minutes * 60 - elapsed, 0)
            return remaining

    def _timer_loop(self) -> None:
        """
        Internal loop that checks for idle timeout and grace period.
        """
        while not self._stop_event.is_set():
            time.sleep(self.check_interval_seconds)
            if self._should_refresh():
                self._perform_refresh()

    def _should_refresh(self) -> bool:
        """
        Determine whether the refresh callback should be invoked.
        """
        with self._lock:
            now = time.time()
            if self._in_grace:
                if now - self._last_activity >= self.grace_period_seconds:
                    return True
                return False
            else:
                if now - self._last_activity >= self.idle_timeout_minutes * 60:
                    self._in_grace = True
                    if self._grace_start_callback:
                        try:
                            self._grace_start_callback()
                        except Exception:
                            pass  # swallow exceptions from grace callback
                return False

    def _perform_refresh(self) -> None:
        """
        Invoke the refresh callback and reset the timer state.
        """
        with self._lock:
            callback = self._refresh_callback
            # Reset state before calling callback to avoid race conditions
            self._last_activity = time.time()
            self._in_grace = False
        if callback:
            try:
                callback()
            except Exception:
                pass  # swallow exceptions from refresh callback