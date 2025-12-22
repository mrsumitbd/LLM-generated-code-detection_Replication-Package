def add_config_arguments(parser: argparse.ArgumentParser, configs: list[str]) -> None:
    for config in configs:
        parser.add_argument(f"--{config}-config", type=str, help=f"Path to {config} config file")