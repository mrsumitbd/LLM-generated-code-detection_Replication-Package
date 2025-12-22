import json

def serialize_config(config):
    """
    Serializes the given configuration dictionary into a JSON string.

    Args:
        config (dict): The configuration dictionary to be serialized.

    Returns:
        str: The JSON string representation of the configuration.
    """
    return json.dumps(config, indent=4)