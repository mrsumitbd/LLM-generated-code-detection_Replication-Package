import logging
from typing import List

def close_loggers(loggers: List[logging.Logger]) -> None:
    """Close all loggers and remove handlers
    
    Args:
        loggers: List of logger instances to close
    """
    for logger in loggers:
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)