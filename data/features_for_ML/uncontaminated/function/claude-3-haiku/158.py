def add_config_arguments(parser: argparse.ArgumentParser, configs: list[str]) -> None:
    """Add CLI arguments for specified config sections.

    Args:
        parser: Argument parser to add config arguments to
        configs: List of config section names to include
    """
    for config in configs:
        group = parser.add_argument_group(f"{config.upper()} Configuration")
        for key, value in config_defaults[config].items():
            if isinstance(value, bool):
                group.add_argument(f"--{config.replace('_', '-')}-{key}", action="store_true", default=value, help=f"{key.replace('_', ' ').capitalize()} (default: {value})")
            else:
                group.add_argument(f"--{config.replace('_', '-')}-{key}", type=type(value), default=value, help=f"{key.replace('_', ' ').capitalize()} (default: {value})")