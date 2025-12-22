import time
import random

WATCH_DOG_TIMEOUT = 5  # Seconds

def is_player_stuck(self):
    """
    Detect if the player is stuck (not moving).
    If stuck for more than WATCH_DOG_TIMEOUT seconds, performs a random action.
    """
    if not self.is_moving():
        if not hasattr(self, '_stuck_start_time'):
            self._stuck_start_time = time.time()
        if time.time() - self._stuck_start_time > WATCH_DOG_TIMEOUT:
            self.perform_random_action()
            self._stuck_start_time = time.time()
    else:
        if hasattr(self, '_stuck_start_time'):
            del self._stuck_start_time