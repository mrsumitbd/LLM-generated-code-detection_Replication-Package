import logging
import os
from typing import Optional

def set_logger(log_file: str) -> None:
    """
    Configure the root logger to write logs to the specified file and to stdout.
    The logger will use INFO level by default and a simple format that includes
    the timestamp, log level, and message.

    Parameters
    ----------
    log_file : str
        Path to the log file. If the directory does not exist, it will be created.
    """
    # Ensure the directory for the log file exists
    log_dir = os.path.dirname(os.path.abspath(log_file))
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    # Avoid adding handlers multiple times if set_logger is called repeatedly
    root_logger = logging.getLogger()
    if root_logger.handlers:
        # Remove existing handlers
        for h in root_logger.handlers[:]:
            root_logger.removeHandler(h)

    # Basic configuration for the root logger
    root_logger.setLevel(logging.INFO)

    # Formatter with timestamp, level, and message
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler
    file_handler: logging.Handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # Stream (stdout) handler
    stream_handler: logging.Handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)