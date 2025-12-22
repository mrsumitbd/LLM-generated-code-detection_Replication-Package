def add_config_arguments(parser: argparse.ArgumentParser, configs: list[str]) -> None:
    """Add CLI arguments for specified config sections.

    Args:
        parser: Argument parser to add config arguments to
        configs: List of config section names to include
    """
    for config in configs:
        parser.add_argument(
            f'--{config}',
            type=str,
            help=f'Configuration for {config}'
        )