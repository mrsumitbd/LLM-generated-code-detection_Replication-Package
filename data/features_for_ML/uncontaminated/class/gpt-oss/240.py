import torch
from typing import Sequence, Optional

class ReachSm:
    """A simple state machine in a robot's task space for a reach task.

    The state machine is implemented as a warp kernel. It takes in the current state of
    the robot's end-effector, and outputs the desired state of the robot's end-effector.
    The state machine is implemented as a finite state machine with the following states:

    1. REST: The robot is at rest.
    2. REACH: The robot reaches to the desired pose. This is the final state.
    """

    # State constants
    REST: int = 0
    REACH: int = 1

    def __init__(self, dt: float, num_envs: int, device: torch.device | str = "cpu"):
        """
        Args:
            dt: Time step (unused in this simple implementation but kept for API compatibility).
            num_envs: Number of parallel environments.
            device: Torch device on which tensors are allocated.
        """
        self.dt = dt
        self.num_envs = num_envs
        self.device = torch.device(device) if isinstance(device, str) else device

        # State tensor: 0 = REST, 1 = REACH
        self.state = torch.full((num_envs,), self.REST, dtype=torch.int32, device=self.device)

    def reset_idx(self, env_ids: Optional[Sequence[int]] = None):
        """
        Reset the state of specified environments to REST.

        Args:
            env_ids: Sequence of environment indices to reset. If None, reset all environments.
        """
        if env_ids is None:
            self.state.fill_(self.REST)
        else:
            idx = torch.tensor(env_ids, device=self.device, dtype=torch.int64)
            self.state[idx] = self.REST

    def compute(self, ee_pose: torch.Tensor, des_final_pose: torch.Tensor) -> torch.Tensor:
        """
        Compute the desired end-effector pose for each environment based on the current state.

        Args:
            ee_pose: Tensor of shape (num_envs, pose_dim) representing the current pose.
            des_final_pose: Tensor of shape (num_envs, pose_dim) representing the desired final pose.

        Returns:
            Tensor of shape (num_envs, pose_dim) containing the desired pose for each environment.
        """
        # Ensure tensors are on the correct device
        ee_pose = ee_pose.to(self.device)
        des_final_pose = des_final_pose.to(self.device)

        # Prepare output tensor
        desired_pose = torch.empty_like(ee_pose)

        # REST state: output current pose and transition to REACH
        rest_mask = self.state == self.REST
        desired_pose[rest_mask] = ee_pose[rest_mask]
        self.state[rest_mask] = self.REACH

        # REACH state: output desired final pose
        reach_mask = self.state == self.REACH
        desired_pose[reach_mask] = des_final_pose[reach_mask]

        return desired_pose