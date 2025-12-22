import logging
import sys

def setup_logging(verbose: bool = False) -> logging.Logger:
    """
    Configure the root logger.

    Parameters
    ----------
    verbose : bool, optional
        If True, set the logging level to DEBUG; otherwise INFO.

    Returns
    -------
    logging.Logger
        The root logger instance.
    """
    level = logging.DEBUG if verbose else logging.INFO
    # Avoid adding multiple handlers if called multiple times
    root = logging.getLogger()
    if root.handlers:
        # Update level if needed
        root.setLevel(level)
        return root

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(formatter)

    root.setLevel(level)
    root.addHandler(handler)
    return root