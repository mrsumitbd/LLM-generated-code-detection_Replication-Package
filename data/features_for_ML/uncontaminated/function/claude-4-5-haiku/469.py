def create_cfg_recursive(cfg, task_args_dict: dict):
    """
    Recursively process a configuration object, replacing placeholders with values from task_args_dict.
    
    Args:
        cfg: Configuration object (can be dict, list, or primitive type)
        task_args_dict: Dictionary containing values to substitute
        
    Returns:
        Processed configuration with substitutions applied
    """
    if isinstance(cfg, dict):
        result = {}
        for key, value in cfg.items():
            result[key] = create_cfg_recursive(value, task_args_dict)
        return result
    elif isinstance(cfg, list):
        return [create_cfg_recursive(item, task_args_dict) for item in cfg]
    elif isinstance(cfg, str):
        # Check if the string is a placeholder in the format ${key} or similar
        if cfg.startswith('${') and cfg.endswith('}'):
            key = cfg[2:-1]
            if key in task_args_dict:
                return task_args_dict[key]
        return cfg
    else:
        return cfg