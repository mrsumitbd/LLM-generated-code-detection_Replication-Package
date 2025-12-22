import json
from collections.abc import Mapping, Iterable

def config_content(config):
    """
    Convert a configuration object into a string representation suitable for
    writing to a configuration file or for comparison in tests.

    Parameters
    ----------
    config : Mapping | Iterable | str | None
        The configuration data. If a mapping, each key/value pair is
        rendered as ``key=value`` on its own line. Keys are sorted
        alphabetically. If a value is a mapping or an iterable (but not a
        string), it is rendered as a JSON string. If ``config`` is a
        string, it is returned unchanged. If ``config`` is ``None``,
        an empty string is returned.

    Returns
    -------
    str
        The string representation of the configuration.
    """
    if config is None:
        return ""

    # If it's already a string, return it as-is
    if isinstance(config, str):
        return config

    # If it's a mapping (dict-like), format key=value lines
    if isinstance(config, Mapping):
        lines = []
        for key in sorted(config):
            value = config[key]
            # Render nested structures as JSON
            if isinstance(value, (Mapping, Iterable)) and not isinstance(value, (str, bytes)):
                value_str = json.dumps(value, sort_keys=True)
            else:
                value_str = str(value)
            lines.append(f"{key}={value_str}")
        return "\n".join(lines)

    # If it's an iterable (but not a string), join elements with commas
    if isinstance(config, Iterable) and not isinstance(config, (str, bytes)):
        return ", ".join(str(item) for item in config)

    # Fallback: just convert to string
    return str(config)