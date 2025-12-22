import logging
from typing import Any

def init_logging(args: Any) -> None:
    """
    Initialize logging for the application.

    The function inspects the provided ``args`` object for common logging
    configuration attributes.  It supports the following optional attributes:

    * ``log_level``   – Logging level as a string (e.g. ``"DEBUG"``) or a
      ``logging`` level constant.  Defaults to ``logging.INFO``.
    * ``log_file``    – Path to a file where logs should be written.  If
      omitted, only console output is produced.
    * ``log_format``  – ``logging`` format string.  Defaults to a
      timestamp‑name‑level‑message format.
    * ``log_datefmt`` – Optional date format string for the formatter.
    * ``log_to_console`` – Boolean flag to enable/disable console output.
      Defaults to ``True``.

    The function removes any pre‑existing handlers on the root logger to
    avoid duplicate log entries.
    """
    # Determine the log level
    level = getattr(args, "log_level", logging.INFO)
    if isinstance(level, str):
        level = level.upper()
        level = getattr(logging, level, logging.INFO)

    # Build the formatter
    fmt = getattr(args, "log_format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    datefmt = getattr(args, "log_datefmt", None)
    formatter = logging.Formatter(fmt, datefmt=datefmt)

    # Prepare handlers list
    handlers = []

    # Console handler (optional)
    if getattr(args, "log_to_console", True):
        console = logging.StreamHandler()
        console.setLevel(level)
        console.setFormatter(formatter)
        handlers.append(console)

    # File handler (optional)
    log_file = getattr(args, "log_file", None)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

    # Configure the root logger
    root = logging.getLogger()
    root.setLevel(level)

    # Remove any existing handlers to avoid duplication
    for h in list(root.handlers):
        root.removeHandler(h)

    # Add the new handlers
    for h in handlers:
        root.addHandler(h)