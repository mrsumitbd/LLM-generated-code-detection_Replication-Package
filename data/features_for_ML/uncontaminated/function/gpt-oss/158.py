import argparse

def add_config_arguments(parser: argparse.ArgumentParser, configs: list[str]) -> None:
    """Add CLI arguments for specified config sections.

    Args:
        parser: Argument parser to add config arguments to
        configs: List of config section names to include
    """
    # Create a dedicated argument group for clarity
    group = parser.add_argument_group("Configuration files")

    for cfg in configs:
        # Use a simple --<section> flag that accepts a file path
        group.add_argument(
            f"--{cfg}",
            dest=cfg,
            type=str,
            help=f"Path to the {cfg} configuration file",
            default=None,
        )