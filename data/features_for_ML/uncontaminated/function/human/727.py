import torch

def _reward_tracking_ang_vel(self):
        # Tracking of angular velocity commands (yaw)
        ang_vel_error = torch.square(self.commands[:, 2] - self.base_ang_vel[:, 2])
        ang_vel_reward = torch.exp(-ang_vel_error / self.reward_cfg["tracking_ang_sigma"])
        if self.command_cfg["zero_stable"]:
            near_zero_mask = (self.commands[:, 0] >= -0.01) & (self.commands[:, 0] <= 0.01)
            if torch.any(near_zero_mask):
                second_error = torch.square(self.commands[near_zero_mask, 2] - self.base_lin_vel[near_zero_mask, 2])
                second_reward = torch.exp(-second_error / self.reward_cfg["tracking_ang_sigma"])
                ang_vel_reward[near_zero_mask] += second_reward
        return ang_vel_reward