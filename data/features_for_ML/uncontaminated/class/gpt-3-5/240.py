import torch
from typing import Sequence

class ReachSm:
    """A simple state machine in a robot's task space for a reach task.

    The state machine is implemented as a warp kernel. It takes in the current state of
    the robot's end-effector, and outputs the desired state of the robot's end-effector.
    The state machine is implemented as a finite state machine with the following states:

    1. REST: The robot is at rest.
    2. REACH: The robot reaches to the desired pose. This is the final state.
    """

    def __init__(self, dt: float, num_envs: int, device: torch.device | str = "cpu"):
        self.dt = dt
        self.num_envs = num_envs
        self.device = device
        self.state = "REST"

    def reset_idx(self, env_ids: Sequence[int] = None):
        pass

    def compute(self, ee_pose: torch.Tensor, des_final_pose: torch.Tensor):
        if self.state == "REST":
            # Perform calculations for transitioning to REACH state
            self.state = "REACH"
            return des_final_pose
        elif self.state == "REACH":
            # Perform calculations for reaching to the desired pose
            return des_final_pose