import torch

def feet_slide(env, sensor_cfg: SceneEntityCfg, asset_cfg: SceneEntityCfg = SceneEntityCfg("robot")) -> torch.Tensor:
    """Penalize feet sliding.

    This function penalizes the agent for sliding its feet on the ground. The reward is computed as the
    norm of the linear velocity of the feet multiplied by a binary contact sensor. This ensures that the
    agent is penalized only when the feet are in contact with the ground.
    """
    # Get the feet contact sensors
    feet_contacts = env.get_contact_forces(sensor_cfg)

    # Get the linear velocity of the feet
    feet_velocities = env.get_linear_velocity(asset_cfg)

    # Compute the feet sliding penalty
    feet_sliding_penalty = torch.sum(torch.norm(feet_velocities, dim=-1) * feet_contacts)

    return feet_sliding_penalty