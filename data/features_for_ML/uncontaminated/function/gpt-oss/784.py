import json
import os
from pathlib import Path
from typing import Any, Dict, Union

def get_options(options_or_path: Union[Dict[str, Any], str, Path]) -> Dict[str, Any]:
    """
    Resolve the provided options or path to a dictionary of options.

    Parameters
    ----------
    options_or_path : dict | str | pathlib.Path
        Either a dictionary of options or a path to a JSON file containing options.

    Returns
    -------
    dict
        The options dictionary.

    Raises
    ------
    TypeError
        If the input is not a dict, str, or Path.
    FileNotFoundError
        If a path is provided but the file does not exist.
    ValueError
        If the file cannot be parsed as JSON.
    """
    # If already a dictionary, return it directly
    if isinstance(options_or_path, dict):
        return options_or_path

    # Resolve Path-like objects to a string path
    if isinstance(options_or_path, Path):
        path = str(options_or_path)
    elif isinstance(options_or_path, str):
        path = options_or_path
    else:
        raise TypeError(
            f"Expected a dict, str, or pathlib.Path, got {type(options_or_path).__name__}"
        )

    # Ensure the file exists
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Options file not found: {path}")

    # Load JSON content
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Failed to parse JSON from {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError(f"Options file {path} does not contain a JSON object")

    return data