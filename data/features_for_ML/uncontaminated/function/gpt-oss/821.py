import logging
import sys
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
    logger = logging.getLogger(name)

    # Avoid adding multiple handlers if this function is called repeatedly
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)

        # Simple structured format: JSON-like string
        formatter = logging.Formatter(
            fmt='{"time":"%(asctime)s","name":"%(name)s","level":"%(levelname)s","msg":"%(message)s"}',
            datefmt="%Y-%m-%dT%H:%M:%S%z"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger