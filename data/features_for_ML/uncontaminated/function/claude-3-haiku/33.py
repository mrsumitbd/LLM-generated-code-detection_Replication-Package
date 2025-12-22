import logging
import os

def set_logger(log_file: str):
    """
    Sets up a logger with the specified log file.

    Args:
        log_file (str): The path to the log file.
    """
    # Create the log directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Configure the logger
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )