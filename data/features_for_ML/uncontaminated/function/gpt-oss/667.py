import torch

def feet_slide(env, sensor_cfg: SceneEntityCfg, asset_cfg: SceneEntityCfg = SceneEntityCfg("robot")) -> torch.Tensor:
    """
    Penalize feet sliding.

    This function penalizes the agent for sliding its feet on the ground. The reward is computed as the
    norm of the linear velocity of the feet multiplied by a binary contact sensor. This ensures that the
    agent is penalized only when the feet are in contact with the ground.
    """
    # Get linear velocity of the feet (shape: [batch, 3])
    feet_vel = env.get_linear_velocity(asset_cfg)

    # Compute L2 norm of the velocity for each batch element
    vel_norm = torch.norm(feet_vel, dim=-1)

    # Get contact sensor data for the feet (shape: [batch, 1] or [batch])
    contact = env.get_contact_sensor(sensor_cfg)

    # Ensure contact is a float tensor of shape [batch]
    if contact.ndim > 1:
        contact = contact.squeeze(-1)
    contact = contact.to(torch.float32)

    # Reward is velocity norm multiplied by contact indicator
    reward = vel_norm * contact

    return reward