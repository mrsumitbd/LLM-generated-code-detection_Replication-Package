import os
import json

def get_cfgs():
    """
    Retrieves configuration settings from a JSON file.

    Returns:
        dict: A dictionary containing the configuration settings.
    """
    config_file = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_file, 'r') as f:
        configs = json.load(f)
    return configs