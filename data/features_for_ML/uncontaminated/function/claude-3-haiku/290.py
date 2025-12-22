import logging
import sys

def setup_logging(verbose=False):
    """
    Sets up the logging configuration for the application.

    Args:
        verbose (bool, optional): If True, sets the logging level to DEBUG. Otherwise, sets it to INFO. Defaults to False.
    """
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )