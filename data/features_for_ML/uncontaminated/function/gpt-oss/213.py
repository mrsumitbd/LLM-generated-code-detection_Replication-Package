def _reward_tracking_ang_vel(self):
    """
    Compute the reward for tracking the commanded angular velocity (yaw).

    The reward is a negative penalty proportional to the squared error between
    the commanded yaw rate (`self._cmd_ang_vel`) and the actual yaw rate
    (`self._ang_vel`). A weight can be applied via the attribute
    `_reward_tracking_ang_vel_weight` if it exists; otherwise a default weight
    of 1.0 is used.

    Returns
    -------
    float
        The tracking reward for the yaw angular velocity.
    """
    # Ensure the required attributes exist
    cmd_ang_vel = getattr(self, "_cmd_ang_vel", 0.0)
    ang_vel = getattr(self, "_ang_vel", 0.0)

    # Compute the error between commanded and actual yaw rate
    error = cmd_ang_vel - ang_vel

    # Optional weight for the reward term
    weight = getattr(self, "_reward_tracking_ang_vel_weight", 1.0)

    # Negative squared error as the reward (penalty for deviation)
    reward = -weight * (error ** 2)

    return reward