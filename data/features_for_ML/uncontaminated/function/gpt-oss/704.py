import logging
from typing import Any

def func_test_logging(app: Any) -> bool:
    """
    Test that the given `app` instance has a working logger.

    The function attempts to retrieve a logger from the app (either via an
    attribute named `logger` or by calling `logging.getLogger` with the
    app's name). It then logs a test message and returns True if no
    exception occurs. If the app does not expose a logger or if logging
    fails, the function returns False.
    """
    try:
        # Try to get a logger from the app
        if hasattr(app, "logger") and isinstance(app.logger, logging.Logger):
            logger = app.logger
        else:
            # Fallback: use the app's name or default logger
            logger_name = getattr(app, "name", None) or getattr(app, "__class__", None).__name__
            logger = logging.getLogger(logger_name)

        # Ensure the logger has at least one handler
        if not logger.handlers:
            # Add a default stream handler if none exist
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        # Log a test message
        logger.debug("func_test_logging: test message")
        return True
    except Exception:
        return False