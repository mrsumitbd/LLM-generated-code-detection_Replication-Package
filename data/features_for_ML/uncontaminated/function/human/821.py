import logging
from typing import Optional

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get a structured logger.

    Loggers by default are logging to stdout, and are expected to be scraped by an
    external process.

    Args:
        name: The name of the logger.

    Returns:
        A logger instance.
    """
    _setup_logger(name)
    return logging.getLogger(name)