import logging
import sys
from typing import Optional

def init_logging(args: Args) -> None:
    """Initialize logging for the application.

    Should be called once when the application starts.
    """
    log_level = getattr(args, 'log_level', 'INFO').upper()
    log_format = getattr(args, 'log_format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_file = getattr(args, 'log_file', None)
    
    numeric_level = getattr(logging, log_level, logging.INFO)
    
    formatter = logging.Formatter(log_format)
    
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)