def load_config_from_path(config_path: Path | str) -> ExtractionConfig:
    if isinstance(config_path, str):
        config_path = Path(config_path)
    
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        if config_path.suffix.lower() == '.json':
            import json
            config_dict = json.load(f)
        elif config_path.suffix.lower() in ['.yaml', '.yml']:
            import yaml
            config_dict = yaml.safe_load(f)
        elif config_path.suffix.lower() == '.toml':
            import tomllib
            config_dict = tomllib.loads(f.read())
        else:
            raise ValueError(f"Unsupported config file format: {config_path.suffix}")
    
    return ExtractionConfig(**config_dict)