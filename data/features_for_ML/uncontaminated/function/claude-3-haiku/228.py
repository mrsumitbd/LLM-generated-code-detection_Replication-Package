import logging
import os

def setup_logger():
    """
    Sets up a basic logger configuration.
    
    Returns:
        logging.Logger: The configured logger instance.
    """
    # Create the logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create the formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Create the file handler
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file = os.path.join(log_dir, 'app.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # Create the stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger