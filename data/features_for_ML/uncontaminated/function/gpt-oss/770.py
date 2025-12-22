import logging
import os
import sys
import json
from datetime import datetime
from typing import Any

try:
    from rich.logging import RichHandler
except ImportError:
    RichHandler = None  # Rich not available


class JSONFormatter(logging.Formatter):
    """Simple JSON formatter for log records."""

    def format(self, record: logging.LogRecord) -> str:
        log_record: dict[str, Any] = {
            "timestamp": datetime.utcfromtimestamp(record.created).isoformat() + "Z",
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_record["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(log_record)


# Global flag to ensure root logger is configured only once
_root_logger_configured = False


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for the specified module.

    This function returns a configured logger that inherits from the root logger
    setup. The logger supports both Rich formatting for human-readable output
    and JSON formatting for machine processing, depending on environment
    configuration.

    Args:
        name: The name of the module, typically __name__.

    Returns:
        A configured Logger instance.
    """
    global _root_logger_configured

    logger = logging.getLogger(name)

    # Configure root logger only once
    if not _root_logger_configured:
        _root_logger_configured = True

        # Determine desired format
        fmt_type = os.getenv("OPENHAND_LOG_FORMAT", "rich").lower()

        # Root logger level
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

        # Create appropriate handler
        if fmt_type == "json":
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(JSONFormatter())
        else:
            # Default to RichHandler if available, otherwise fallback to StreamHandler
            if RichHandler is not None:
                handler = RichHandler(rich_tracebacks=True, show_path=False)
            else:
                handler = logging.StreamHandler(sys.stdout)
                handler.setFormatter(logging.Formatter("%(message)s"))

        handler.setLevel(logging.DEBUG)
        root_logger.addHandler(handler)

    # Ensure the logger inherits handlers from root
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        # Inherit handlers from root
        logger.handlers = logging.getLogger().handlers
        logger.propagate = False

    return logger