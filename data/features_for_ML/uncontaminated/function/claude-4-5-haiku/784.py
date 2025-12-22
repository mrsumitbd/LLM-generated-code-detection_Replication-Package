import json
import os
from pathlib import Path


def get_options(options_or_path):
    """
    Get options from either a dictionary or a file path.
    
    Args:
        options_or_path: Either a dictionary of options or a string path to a JSON file
        
    Returns:
        A dictionary of options
    """
    if isinstance(options_or_path, dict):
        return options_or_path
    
    if isinstance(options_or_path, str):
        path = Path(options_or_path)
        
        if path.exists() and path.is_file():
            with open(path, 'r') as f:
                return json.load(f)
        
        try:
            return json.loads(options_or_path)
        except json.JSONDecodeError:
            pass
    
    return {}