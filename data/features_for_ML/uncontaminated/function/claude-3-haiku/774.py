import logging
import os
from typing import Optional

def get_logger(name: str, component: Optional[str] = None) -> logging.Logger:
    """
    Get a logger with the specified name.
    
    Args:
        name: The name of the logger, typically __name__ of the calling module
        component: Optional component name to determine log file (server, ui, tts, stt)
                  If None, it will be inferred from the name
    
    Returns:
        A configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if component is None:
        component = name.split('.')[-1]

    log_dir = os.path.join('logs', component)
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f'{component}.log')

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger