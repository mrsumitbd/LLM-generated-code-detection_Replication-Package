class PoseObservationsCfg:
    """Observation specifications for the environment."""

    def __init__(self, num_joints: int, joint_names: list[str], joint_limits: list[tuple[float, float]],
                 root_name: str, root_limits: tuple[float, float], root_position_limits: tuple[float, float, float],
                 root_orientation_limits: tuple[float, float, float], end_effector_names: list[str],
                 end_effector_limits: list[tuple[float, float, float]]):
        self.num_joints = num_joints
        self.joint_names = joint_names
        self.joint_limits = joint_limits
        self.root_name = root_name
        self.root_limits = root_limits
        self.root_position_limits = root_position_limits
        self.root_orientation_limits = root_orientation_limits
        self.end_effector_names = end_effector_names
        self.end_effector_limits = end_effector_limits

    def get_joint_limits(self, joint_index: int) -> tuple[float, float]:
        """Get the limits for a specific joint."""
        return self.joint_limits[joint_index]

    def get_root_limits(self) -> tuple[float, float]:
        """Get the limits for the root."""
        return self.root_limits

    def get_root_position_limits(self) -> tuple[float, float, float]:
        """Get the limits for the root position."""
        return self.root_position_limits

    def get_root_orientation_limits(self) -> tuple[float, float, float]:
        """Get the limits for the root orientation."""
        return self.root_orientation_limits

    def get_end_effector_limits(self, end_effector_index: int) -> tuple[float, float, float]:
        """Get the limits for a specific end-effector."""
        return self.end_effector_limits[end_effector_index]