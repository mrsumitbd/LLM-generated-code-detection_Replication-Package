import json
import os

def get_options(options_or_path):
    if isinstance(options_or_path, dict):
        return options_or_path
    elif os.path.isfile(options_or_path):
        with open(options_or_path, 'r') as f:
            return json.load(f)
    else:
        raise ValueError("Invalid input: options_or_path must be a dictionary or a file path")