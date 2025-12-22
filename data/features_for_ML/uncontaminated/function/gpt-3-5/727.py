def _reward_tracking_ang_vel(self):
    ang_vel_error = self.target_ang_vel - self.current_ang_vel
    reward = 1.0 - abs(ang_vel_error)
    return reward