import time

def is_player_stuck(self):
    """
    Detect if the player is stuck (not moving).
    If stuck for more than WATCH_DOG_TIMEOUT seconds, performs a random action.
    """
    # Ensure we have a timestamp for the last movement check
    now = time.time()

    # Initialize tracking attributes if they don't exist
    if not hasattr(self, "_last_position"):
        self._last_position = getattr(self, "position", None)
        self._last_move_time = now
        return False

    # Get current position (assumes a `position` attribute exists)
    current_pos = getattr(self, "position", None)

    # If the position hasn't changed, check how long we've been stuck
    if current_pos == self._last_position:
        if now - self._last_move_time > getattr(self, "WATCH_DOG_TIMEOUT", 5):
            # Perform a random action to try to get unstuck
            if hasattr(self, "random_action"):
                self.random_action()
            else:
                # Fallback: try a random move if available
                if hasattr(self, "move_randomly"):
                    self.move_randomly()
            # Reset the timer to avoid repeated actions
            self._last_move_time = now
            return True
    else:
        # Player has moved; update tracking info
        self._last_position = current_pos
        self._last_move_time = now

    return False