import random

def is_player_stuck(self):
    if self.player_speed == 0:
        if self.stuck_timer is None:
            self.stuck_timer = time.time()
        else:
            if time.time() - self.stuck_timer > WATCH_DOG_TIMEOUT:
                self.perform_random_action()
    else:
        self.stuck_timer = None