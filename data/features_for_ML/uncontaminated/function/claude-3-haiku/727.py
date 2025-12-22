def _reward_tracking_ang_vel(self):
    # Tracking of angular velocity commands (yaw)
    if self.target_ang_vel is not None:
        ang_vel_error = self.target_ang_vel - self.ang_vel
        self.ang_vel_error_sum += ang_vel_error
        self.ang_vel_error_sum = max(-self.ang_vel_error_max, min(self.ang_vel_error_max, self.ang_vel_error_sum))
        self.ang_vel_error_list.append(ang_vel_error)
        if len(self.ang_vel_error_list) > self.ang_vel_error_history:
            self.ang_vel_error_list.pop(0)
        self.ang_vel_reward = -np.abs(ang_vel_error) - 0.1 * np.abs(self.ang_vel_error_sum)
    else:
        self.ang_vel_reward = 0.0
    return self.ang_vel_reward