import logging
from typing import Union

# Assuming CommonParameters is defined elsewhere with an optional `log_level` attribute.
# If it is not available, we simply ignore the argument.

def set_logging_level(common: Union["CommonParameters", None] = None) -> None:
    """
    Configure the root logger level based on the provided CommonParameters instance.
    If `common` is None or does not provide a valid `log_level`, the default level
    is set to INFO.
    """
    # Default level
    level = logging.INFO

    # Try to extract a log level from the common parameters
    if common is not None:
        # CommonParameters may expose `log_level` as a string or an int
        log_level_attr = getattr(common, "log_level", None)
        if log_level_attr is not None:
            # If it's already an int, use it directly
            if isinstance(log_level_attr, int):
                level = log_level_attr
            else:
                # Assume it's a string like "debug", "INFO", etc.
                level_name = str(log_level_attr).upper()
                # Resolve the string to a logging level constant
                resolved = getattr(logging, level_name, None)
                if isinstance(resolved, int):
                    level = resolved
                else:
                    # Fallback: try to interpret numeric strings
                    try:
                        level = int(log_level_attr)
                    except Exception:
                        # Keep default if resolution fails
                        pass

    # Configure the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # If no handlers are configured yet, add a basic handler
    if not root_logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)