import time
from typing import Callable, Optional

class RefreshTimer:
    """
    Manages automatic page refresh based on activity tracking.
    
    This class implements a two-stage timer system:
    1. Idle timeout: Wait for configured minutes of inactivity
    2. Grace period: Wait additional seconds before actually refreshing
    
    The timer resets whenever activity is detected.
    """

    def __init__(self):
        self._idle_timeout = 5 * 60  # 5 minutes
        self._grace_period = 10  # 10 seconds
        self._last_activity_time = time.time()
        self._refresh_callback = None
        self._grace_period_start_callback = None
        self._timer_thread = None
        self._running = False

    def _apply_humanization(self, value: int, min_value: int) -> int:
        """
        Applies a simple humanization to the given value.
        If the value is less than the minimum, it returns the minimum.
        """
        return max(value, min_value)

    def start(self, refresh_callback: Callable, grace_period_start_callback: Optional[Callable] = None) -> None:
        """
        Starts the refresh timer.
        """
        self._refresh_callback = refresh_callback
        self._grace_period_start_callback = grace_period_start_callback
        self._running = True
        self._timer_loop()

    def stop(self) -> None:
        """
        Stops the refresh timer.
        """
        self._running = False

    def record_activity(self) -> None:
        """
        Records user activity, resetting the timer.
        """
        self._last_activity_time = time.time()

    def is_running(self) -> bool:
        """
        Returns whether the timer is currently running.
        """
        return self._running

    def is_in_grace_period(self) -> bool:
        """
        Returns whether the timer is currently in the grace period.
        """
        return time.time() - self._last_activity_time >= self._idle_timeout

    def get_time_until_next_check(self) -> float:
        """
        Returns the time in seconds until the next timer check.
        """
        time_since_last_activity = time.time() - self._last_activity_time
        time_until_next_check = self._idle_timeout - time_since_last_activity
        return self._apply_humanization(time_until_next_check, 0.0)

    def _timer_loop(self) -> None:
        """
        The main timer loop that checks for inactivity and triggers the refresh.
        """
        while self._running:
            time_until_next_check = self.get_time_until_next_check()
            if time_until_next_check <= 0:
                if self._should_refresh():
                    self._perform_refresh()
                else:
                    self.record_activity()
            time.sleep(1)

    def _should_refresh(self) -> bool:
        """
        Determines whether a refresh should be performed.
        """
        return time.time() - self._last_activity_time >= self._idle_timeout + self._grace_period

    def _perform_refresh(self) -> None:
        """
        Performs the actual refresh and notifies the callbacks.
        """
        if self._grace_period_start_callback:
            self._grace_period_start_callback()
        self._refresh_callback()
        self.record_activity()