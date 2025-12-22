import logging

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
    logger.propagate = True
    return logger