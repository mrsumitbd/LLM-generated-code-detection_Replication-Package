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
        self.device = device if isinstance(device, torch.device) else torch.device(device)
        
        # State machine states: 0 = REST, 1 = REACH
        self.state = torch.zeros(num_envs, dtype=torch.long, device=self.device)
        
        # Desired pose for each environment
        self.des_pose = torch.zeros((num_envs, 7), dtype=torch.float32, device=self.device)
        
        # Current desired pose output
        self.des_pose_out = torch.zeros((num_envs, 7), dtype=torch.float32, device=self.device)

    def reset_idx(self, env_ids: Sequence[int] = None):
        if env_ids is None:
            env_ids = list(range(self.num_envs))
        
        env_ids = torch.tensor(env_ids, dtype=torch.long, device=self.device)
        
        # Reset state to REST
        self.state[env_ids] = 0
        
        # Reset desired pose
        self.des_pose[env_ids] = 0.0
        self.des_pose_out[env_ids] = 0.0

    def compute(self, ee_pose: torch.Tensor, des_final_pose: torch.Tensor):
        """Compute the desired pose based on current state and final desired pose.
        
        Args:
            ee_pose: Current end-effector pose (num_envs, 7) [pos(3), quat(4)]
            des_final_pose: Desired final pose (num_envs, 7) [pos(3), quat(4)]
        
        Returns:
            des_pose_out: Desired pose output (num_envs, 7)
        """
        # Update desired final pose
        self.des_pose = des_final_pose.clone()
        
        # For REST state, output current pose
        # For REACH state, output desired final pose
        rest_mask = self.state == 0
        reach_mask = self.state == 1
        
        # Initialize output with current pose
        self.des_pose_out = ee_pose.clone()
        
        # For environments in REACH state, output the desired final pose
        self.des_pose_out[reach_mask] = self.des_pose[reach_mask]
        
        # Transition logic: move from REST to REACH
        # In a simple implementation, we transition immediately
        self.state[rest_mask] = 1
        
        return self.des_pose_out