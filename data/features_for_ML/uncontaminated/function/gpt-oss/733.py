import logging

def _setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Configure the root logger with a NullHandler to avoid duplicate logs and
    return a named logger with the specified level.
    """
    # Ensure the root logger has only a NullHandler
    root = logging.getLogger()
    root.handlers = []                     # Remove any existing handlers
    root.addHandler(logging.NullHandler()) # Add a NullHandler
    root.setLevel(level)

    # Create or get the named logger and set its level
    logger = logging.getLogger(name)
    logger.setLevel(level)

    return logger