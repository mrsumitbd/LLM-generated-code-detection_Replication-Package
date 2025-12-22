import argparse
import json
import logging
import os
import sys
from typing import List, Any


def initialize_app(param: Any, args: List[str] = None):
    """
    Initialize app
    If you use gunicorn as a process manager, initialize_app can be invoke in
    `on_starting` hook.
    Args:
        param: WebWerverParameters (any object that will receive the loaded config)
        args: List[str] (command‑line arguments, defaults to sys.argv[1:])
    """
    # Use provided args or fall back to sys.argv
    if args is None:
        args = sys.argv[1:]

    # Basic argument parsing
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--config",
        dest="config_file",
        default=getattr(param, "config_file", None),
        help="Path to JSON configuration file",
    )
    parser.add_argument(
        "--debug",
        dest="debug",
        action="store_true",
        default=getattr(param, "debug", False),
        help="Enable debug mode",
    )
    # Parse only the known arguments; ignore the rest
    parsed, _ = parser.parse_known_args(args)

    # Load configuration file if specified
    config_data = {}
    if parsed.config_file:
        try:
            with open(parsed.config_file, "r", encoding="utf-8") as f:
                config_data = json.load(f)
        except Exception as exc:
            logging.error(
                f"Failed to load configuration file '{parsed.config_file}': {exc}"
            )

    # Configure logging
    log_level = logging.DEBUG if parsed.debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Store the loaded configuration and debug flag back into param
    setattr(param, "config", config_data)
    setattr(param, "debug", parsed.debug)

    # Export debug flag to environment for downstream consumers
    os.environ["APP_DEBUG"] = str(parsed.debug)

    return param