import json
import os
from typing import Any

# Load configuration from a JSON file if it exists
_CONFIG: dict[str, Any] = {}
_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
if os.path.isfile(_CONFIG_PATH):
    try:
        with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
            _CONFIG = json.load(f)
    except Exception:
        _CONFIG = {}

def get_setting(tab: str, key: str, default: Any = None) -> Any:
    """
    Retrieve a setting value from the configuration.

    Parameters
    ----------
    tab : str
        The top-level section of the configuration.
    key : str
        The key within the section.
    default : Any, optional
        The value to return if the setting is not found.

    Returns
    -------
    Any
        The configuration value or the default.
    """
    # Environment variable override (e.g., TAB_KEY)
    env_var = f"{tab.upper()}_{key.upper()}"
    if env_var in os.environ:
        return os.environ[env_var]

    # Retrieve from the loaded JSON configuration
    section = _CONFIG.get(tab, {})
    if isinstance(section, dict):
        return section.get(key, default)

    return default