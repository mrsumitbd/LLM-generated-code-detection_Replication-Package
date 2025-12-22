def feet_slide(env, sensor_cfg: SceneEntityCfg, asset_cfg: SceneEntityCfg = SceneEntityCfg("robot")) -> torch.Tensor:
    """Penalize feet sliding.

    This function penalizes the agent for sliding its feet on the ground. The reward is computed as the
    norm of the linear velocity of the feet multiplied by a binary contact sensor. This ensures that the
    agent is penalized only when the feet are in contact with the ground.
    """
    # Get the asset (robot)
    asset = env.scene[asset_cfg.name]
    
    # Get the sensor (contact sensor on feet)
    sensor = env.scene[sensor_cfg.name]
    
    # Get the linear velocity of the feet
    feet_vel = sensor.data.lin_vel_w
    
    # Compute the norm of the linear velocity
    feet_vel_norm = torch.norm(feet_vel, dim=-1)
    
    # Get the contact state from the sensor
    # The contact sensor returns a binary tensor indicating contact
    contact = sensor.data.is_in_contact.float()
    
    # Penalize sliding: multiply velocity norm by contact state
    # This penalizes only when feet are in contact with ground
    penalty = feet_vel_norm * contact
    
    return penalty