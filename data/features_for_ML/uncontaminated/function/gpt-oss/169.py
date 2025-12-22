from pathlib import Path
from typing import Dict

def get_file_content(
    filepath: Path
) -> Dict[str, str]:
    """
    Get content of a file.
    Args:
        filepath: Path to a file
    Returns:
        A dictionary with a single key 'content' containing the file content as a string.
    Raises:
        IOError: if read content of `filepath` failed
    """
    try:
        content = filepath.read_text(encoding="utf-8")
    except OSError as exc:
        raise IOError(f"Failed to read file {filepath}") from exc
    return {"content": content}