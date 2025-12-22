import json
from collections.abc import Mapping

def serialize_config(config):
    """
    Serialize a configuration object into a JSON string.

    Parameters
    ----------
    config : Mapping or any JSON‑serialisable object
        The configuration to serialize.

    Returns
    -------
    str
        A JSON representation of the configuration. If the object is not
        directly serialisable, its string representation is returned.
    """
    # If the config is a mapping, ensure it is serialisable
    if isinstance(config, Mapping):
        try:
            return json.dumps(config, sort_keys=True, separators=(",", ":"))
        except (TypeError, OverflowError):
            # Fallback: convert to string
            return str(config)

    # For non‑mapping objects, attempt direct serialization
    try:
        return json.dumps(config, sort_keys=True, separators=(",", ":"))
    except (TypeError, OverflowError):
        # Fallback: use the object's string representation
        return str(config)