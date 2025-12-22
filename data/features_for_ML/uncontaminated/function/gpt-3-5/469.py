def create_cfg_recursive(cfg, task_args_dict: dict):
    for key, value in task_args_dict.items():
        if isinstance(value, dict):
            sub_cfg = cfg.setdefault(key, {})
            create_cfg_recursive(sub_cfg, value)
        else:
            cfg[key] = value