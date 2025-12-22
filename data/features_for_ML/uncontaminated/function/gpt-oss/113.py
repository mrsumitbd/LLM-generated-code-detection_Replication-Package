import logging
from typing import List

def close_loggers(loggers: List[logging.Logger]) -> None:
    """Close all loggers and remove handlers

    Args:
        loggers: List of logger instances to close
    """
    for logger in loggers:
        # Copy the list to avoid modification during iteration
        for handler in list(logger.handlers):
            try:
                # Some handlers (e.g., FileHandler) have a close method
                handler.close()
            except Exception:
                # Ignore errors during close
                pass
            # Remove the handler from the logger
            logger.removeHandler(handler)
        # Ensure the handlers list is empty
        logger.handlers.clear()