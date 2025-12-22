import json
import os
from typing import Any

def dump_distro_mapping(path: str) -> None:
    """
    Load a distro mapping file (JSON or YAML) and print it as pretty JSON.

    Parameters
    ----------
    path : str
        Path to the mapping file.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If the file cannot be parsed as JSON or YAML.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Mapping file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Try JSON first
    try:
        mapping: Any = json.loads(content)
    except json.JSONDecodeError:
        # Fallback to YAML if available
        try:
            import yaml  # type: ignore
            mapping = yaml.safe_load(content)
        except Exception as exc:
            raise ValueError(
                f"File '{path}' is neither valid JSON nor YAML: {exc}"
            ) from exc

    # Pretty‑print the mapping as JSON
    print(json.dumps(mapping, indent=2, sort_keys=True))