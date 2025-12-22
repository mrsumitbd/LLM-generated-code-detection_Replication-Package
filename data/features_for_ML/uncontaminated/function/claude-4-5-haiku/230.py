def is_player_stuck(self):
    """
    Detect if the player is stuck (not moving).
    If stuck for more than WATCH_DOG_TIMEOUT seconds, performs a random action.
    """
    import time
    import random
    
    current_pos = self.player.pos
    current_time = time.time()
    
    if not hasattr(self, '_last_pos'):
        self._last_pos = current_pos
        self._last_check_time = current_time
        return False
    
    time_elapsed = current_time - self._last_check_time
    
    if time_elapsed >= 1.0:
        if current_pos == self._last_pos:
            if not hasattr(self, '_stuck_start_time'):
                self._stuck_start_time = current_time
            
            stuck_duration = current_time - self._stuck_start_time
            
            if stuck_duration > self.WATCH_DOG_TIMEOUT:
                actions = ['up', 'down', 'left', 'right', 'jump']
                random_action = random.choice(actions)
                self.perform_action(random_action)
                self._stuck_start_time = current_time
                return True
        else:
            self._stuck_start_time = current_time
        
        self._last_pos = current_pos
        self._last_check_time = current_time
    
    return False