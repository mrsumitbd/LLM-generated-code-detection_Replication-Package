import json
import os
from pathlib import Path
from typing import Any, Dict

def get_blend_data() -> Dict[str, Any]:
    """
    Load blend data from a JSON file named `blend_data.json` located in the current working directory.
    If the file does not exist or cannot be parsed, an empty dictionary is returned.

    Returns:
        dict: The parsed blend data, or an empty dict if unavailable.
    """
    # Determine the path to the blend data file
    blend_file = Path.cwd() / "blend_data.json"

    # If the file exists, attempt to load and parse it
    if blend_file.is_file():
        try:
            with blend_file.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            # If parsing fails or the file cannot be read, fall back to empty dict
            pass

    # Default return value if file is missing or unreadable
    return {}