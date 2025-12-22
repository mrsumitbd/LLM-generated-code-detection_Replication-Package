def _reward_tracking_ang_vel(self):
    # Tracking of angular velocity commands (yaw)
    desired_yaw_rate = self.desired_yaw_rate
    current_yaw_rate = self.current_yaw_rate
    error_yaw_rate = desired_yaw_rate - current_yaw_rate
    reward_yaw_rate = 1.0 - abs(error_yaw_rate)
    
    return reward_yaw_rate