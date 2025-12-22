import torch

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
        self.device = torch.device(device)
        self.state = torch.zeros(self.num_envs, dtype=torch.long, device=self.device)
        self.reached_goal = torch.zeros(self.num_envs, dtype=torch.bool, device=self.device)

    def reset_idx(self, env_ids: Sequence[int] = None):
        if env_ids is None:
            self.state.fill_(0)
            self.reached_goal.fill_(False)
        else:
            self.state[env_ids] = 0
            self.reached_goal[env_ids] = False

    def compute(self, ee_pose: torch.Tensor, des_final_pose: torch.Tensor):
        # Compute the desired end-effector pose
        desired_ee_pose = torch.zeros_like(ee_pose)

        # Update the state machine
        self.state[~self.reached_goal] += 1
        self.reached_goal = self.state >= 1

        # Set the desired end-effector pose based on the state
        desired_ee_pose[~self.reached_goal] = ee_pose[~self.reached_goal]
        desired_ee_pose[self.reached_goal] = des_final_pose[self.reached_goal]

        return desired_ee_pose