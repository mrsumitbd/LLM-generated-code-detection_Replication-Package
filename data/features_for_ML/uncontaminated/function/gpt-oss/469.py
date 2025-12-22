def create_cfg_recursive(cfg, task_args_dict: dict):
    """
    Recursively merge `task_args_dict` into `cfg`.  
    For each key in `task_args_dict`:
        * If the value is a dict, merge it into the corresponding dict in `cfg`
          (creating a new dict if necessary).
        * Otherwise, set the value directly in `cfg`.

    The function returns the updated `cfg` object.
    """
    for key, value in task_args_dict.items():
        if isinstance(value, dict):
            # Ensure the target is a dict
            sub_cfg = cfg.get(key)
            if not isinstance(sub_cfg, dict):
                sub_cfg = {}
            cfg[key] = create_cfg_recursive(sub_cfg, value)
        else:
            cfg[key] = value
    return cfg