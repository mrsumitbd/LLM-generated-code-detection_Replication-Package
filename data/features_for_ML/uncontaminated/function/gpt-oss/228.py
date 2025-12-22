import logging
import os

def setup_logger():
    """
    Set up and return a configured logger.

    The logger is named 'app', logs at INFO level, and writes to both
    stdout and a file named 'app.log' in the current working directory.
    If the logger has already been configured, the existing instance is returned.
    """
    logger_name = "app"
    logger = logging.getLogger(logger_name)

    # If the logger is already configured, just return it
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # Formatter for both handlers
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Stream handler (stdout)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # File handler
    log_file = os.path.join(os.getcwd(), "app.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger