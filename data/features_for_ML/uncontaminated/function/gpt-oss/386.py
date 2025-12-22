import logging
import logging.config
from typing import Any, Dict, Union

# Assuming LoggerConfigData is a user‑defined type that can be converted to a dict.
# It may expose a `config` attribute, a `to_dict()` method, or be a plain dict itself.
def _to_dict(obj: Any) -> Dict[str, Any]:
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, "config") and isinstance(obj.config, dict):
        return obj.config
    if hasattr(obj, "to_dict") and callable(obj.to_dict):
        return obj.to_dict()
    raise TypeError("Unsupported LoggerConfigData type: %r" % obj)

def config_loggers(in_logger_config: Any) -> None:
    """
    Configure the Python logging system based on the supplied configuration data.

    Parameters
    ----------
    in_logger_config : LoggerConfigData
        Configuration data that can be converted to a dictionary compatible with
        `logging.config.dictConfig`.  The function accepts either a plain dict,
        an object with a `config` attribute, or an object with a `to_dict()` method.

    Returns
    -------
    None
    """
    if in_logger_config is None:
        return

    try:
        config_dict = _to_dict(in_logger_config)
    except Exception as exc:
        logging.getLogger(__name__).error(
            "Failed to convert logger configuration to dict: %s", exc
        )
        return

    try:
        logging.config.dictConfig(config_dict)
    except Exception as exc:
        logging.getLogger(__name__).error(
            "Failed to apply logger configuration: %s", exc
        )