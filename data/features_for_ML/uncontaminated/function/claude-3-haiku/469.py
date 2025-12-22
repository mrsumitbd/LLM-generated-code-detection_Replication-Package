def create_cfg_recursive(cfg, task_args_dict: dict):
    for task, args in task_args_dict.items():
        if isinstance(args, dict):
            cfg = create_cfg_recursive(cfg, args)
        else:
            cfg.add_task(task, args)
    return cfg