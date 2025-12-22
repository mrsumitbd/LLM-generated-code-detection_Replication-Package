import threading
import time
from typing import Callable, Optional
import random


class RefreshTimer:
    """
    Manages automatic page refresh based on activity tracking.
    
    This class implements a two-stage timer system:
    1. Idle timeout: Wait for configured minutes of inactivity
    2. Grace period: Wait additional seconds before actually refreshing
    
    The timer resets whenever activity is detected.
    """

    def __init__(self):
        self._idle_timeout_minutes = 30
        self._grace_period_seconds = 60
        self._last_activity_time = time.time()
        self._running = False
        self._in_grace_period = False
        self._timer_thread = None
        self._lock = threading.Lock()
        self._refresh_callback = None
        self._grace_period_start_callback = None

    def _apply_humanization(self, value: int, min_value: int) -> int:
        """Apply random humanization to a value to avoid predictable patterns."""
        if value <= min_value:
            return value
        variance = max(1, int(value * 0.1))
        return value + random.randint(-variance, variance)

    def start(self, refresh_callback: Callable, grace_period_start_callback: Optional[Callable] = None) -> None:
        """Start the refresh timer with the provided callbacks."""
        with self._lock:
            if self._running:
                return
            
            self._refresh_callback = refresh_callback
            self._grace_period_start_callback = grace_period_start_callback
            self._last_activity_time = time.time()
            self._in_grace_period = False
            self._running = True
        
        self._timer_thread = threading.Thread(target=self._timer_loop, daemon=True)
        self._timer_thread.start()

    def stop(self) -> None:
        """Stop the refresh timer."""
        with self._lock:
            self._running = False

    def record_activity(self) -> None:
        """Record user activity and reset the timer."""
        with self._lock:
            self._last_activity_time = time.time()
            self._in_grace_period = False

    def is_running(self) -> bool:
        """Check if the timer is currently running."""
        with self._lock:
            return self._running

    def is_in_grace_period(self) -> bool:
        """Check if the timer is in the grace period."""
        with self._lock:
            return self._in_grace_period

    def get_time_until_next_check(self) -> float:
        """Get the time in seconds until the next check."""
        with self._lock:
            if not self._running:
                return 0
            
            elapsed = time.time() - self._last_activity_time
            idle_timeout_seconds = self._idle_timeout_minutes * 60
            
            if self._in_grace_period:
                grace_elapsed = elapsed - idle_timeout_seconds
                return max(0, self._grace_period_seconds - grace_elapsed)
            else:
                return max(0, idle_timeout_seconds - elapsed)

    def _timer_loop(self) -> None:
        """Main timer loop that runs in a separate thread."""
        while True:
            with self._lock:
                if not self._running:
                    break
            
            time.sleep(1)
            
            if self._should_refresh():
                self._perform_refresh()

    def _should_refresh(self) -> bool:
        """Check if a refresh should be performed."""
        with self._lock:
            if not self._running:
                return False
            
            elapsed = time.time() - self._last_activity_time
            idle_timeout_seconds = self._idle_timeout_minutes * 60
            
            if not self._in_grace_period:
                if elapsed >= idle_timeout_seconds:
                    self._in_grace_period = True
                    if self._grace_period_start_callback:
                        self._grace_period_start_callback()
                    return False
            else:
                grace_elapsed = elapsed - idle_timeout_seconds
                if grace_elapsed >= self._grace_period_seconds:
                    return True
            
            return False

    def _perform_refresh(self) -> None:
        """Perform the refresh action."""
        with self._lock:
            if self._running and self._refresh_callback:
                callback = self._refresh_callback
        
        try:
            callback()
        except Exception:
            pass
        
        with self._lock:
            self._last_activity_time = time.time()
            self._in_grace_period = False