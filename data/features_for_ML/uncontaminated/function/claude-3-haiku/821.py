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
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger