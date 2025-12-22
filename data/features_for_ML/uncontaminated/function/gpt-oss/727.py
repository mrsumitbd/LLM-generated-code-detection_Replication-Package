def _reward_tracking_ang_vel(self):
    """
    Compute a reward for tracking the commanded angular velocity (yaw).

    The reward is defined as the negative squared error between the commanded
    yaw angular velocity and the actual yaw angular velocity.  A smaller error
    yields a higher (less negative) reward.

    Returns
    -------
    float
        The reward value for the current timestep.
    """
    # Ensure the required attributes exist
    if not hasattr(self, "_ang_vel_cmd") or not hasattr(self, "_ang_vel"):
        return 0.0

    # Yaw is assumed to be the third component (index 2)
    try:
        cmd_yaw = float(self._ang_vel_cmd[2])
        actual_yaw = float(self._ang_vel[2])
    except (IndexError, TypeError):
        # If the arrays are not the expected shape, return zero reward
        return 0.0

    # Compute squared error and return negative value as reward
    error = cmd_yaw - actual_yaw
    reward = - (error ** 2)
    return float(reward)