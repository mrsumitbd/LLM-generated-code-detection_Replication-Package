def feet_slide(env, sensor_cfg: SceneEntityCfg, asset_cfg=SceneEntityCfg("robot")):
    linear_velocity = env.get_asset_linear_velocity(asset_cfg)
    contact_sensor = env.get_sensor(sensor_cfg)
    return torch.norm(linear_velocity) * contact_sensor