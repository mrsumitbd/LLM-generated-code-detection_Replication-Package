def _reward_tracking_ang_vel(self):
    # Tracking of angular velocity commands (yaw)
    # Penalize the difference between commanded and actual angular velocity
    ang_vel_error = torch.norm(
        self.commands[:, 2:3] - self.base_ang_vel[:, 2:3], dim=1
    )
    return torch.exp(-ang_vel_error / self.cfg.rewards.tracking_ang_vel_error_scale)