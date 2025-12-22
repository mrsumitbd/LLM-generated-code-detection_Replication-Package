import logging
import os
from typing import Optional

from rich.logging import RichHandler

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for the specified module.

    This function returns a configured logger that inherits from the root logger
    setup. The logger supports both Rich formatting for human-readable output
    and JSON formatting for machine processing, depending on environment configuration.

    Args:
        name: The name of the module, typically __name__.

    Returns:
        A configured Logger instance.

    Example:
        >>> from openhands.sdk.logger import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("This is an info message")
        >>> logger.error("This is an error message")
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Check if the environment variable is set to enable JSON logging
    json_logging = os.getenv("JSON_LOGGING", "false").lower() == "true"

    if json_logging:
        # Configure the logger for JSON output
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
    else:
        # Configure the logger for Rich formatting
        formatter = RichHandler(
            rich_tracebacks=True,
            tracebacks_show_locals=True,
            show_time=True,
            show_path=False,
        )
        handler = formatter

    logger.addHandler(handler)
    return logger