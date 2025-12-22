from typing import Callable, Optional
import time

class RefreshTimer:
    """
    Manages automatic page refresh based on activity tracking.
    
    This class implements a two-stage timer system:
    1. Idle timeout: Wait for configured minutes of inactivity
    2. Grace period: Wait additional seconds before actually refreshing
    
    The timer resets whenever activity is detected.
    """

    def __init__(self):
        self.idle_timeout_minutes = 5
        self.grace_period_seconds = 10
        self.last_activity_time = time.time()
        self.running = False

    def _apply_humanization(self, value: int, min_value: int) -> int:
        return max(value, min_value)

    def start(self, refresh_callback: Callable, grace_period_start_callback: Optional[Callable] = None) -> None:
        self.refresh_callback = refresh_callback
        self.grace_period_start_callback = grace_period_start_callback
        self.running = True
        self._timer_loop()

    def stop(self) -> None:
        self.running = False

    def record_activity(self) -> None:
        self.last_activity_time = time.time()

    def is_running(self) -> bool:
        return self.running

    def is_in_grace_period(self) -> bool:
        return time.time() - self.last_activity_time < self.grace_period_seconds

    def get_time_until_next_check(self) -> float:
        return max(0, self.idle_timeout_minutes * 60 - (time.time() - self.last_activity_time))

    def _timer_loop(self) -> None:
        while self.running:
            if self._should_refresh():
                self._perform_refresh()
            time.sleep(1)

    def _should_refresh(self) -> bool:
        return time.time() - self.last_activity_time >= self.idle_timeout_minutes * 60

    def _perform_refresh(self) -> None:
        if self.grace_period_start_callback:
            self.grace_period_start_callback()
            time.sleep(self.grace_period_seconds)
        self.refresh_callback()
        self.last_activity_time = time.time()