import logging
import sys
from logging.handlers import RotatingFileHandler

def init_logging(args: Args) -> None:
    """Initialize logging for the application.

    Should be called once when the application starts.
    """
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            RotatingFileHandler(args.log_file, maxBytes=10 * 1024 * 1024, backupCount=5),
            logging.StreamHandler(sys.stdout),
        ],
    )