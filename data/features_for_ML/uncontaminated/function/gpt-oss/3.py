import re
from pathlib import Path
from typing import List, Optional

def _enumerate_files(
    paths: List[str],
    valid_file_extension: str,
    exclude_pattern: Optional[str] = None,
    recursive: bool = False,
) -> List[Path]:
    """
    Enumerate files in a folder based on include and exclude patterns.

    Args:
        paths: paths to the folders to traverse, these will be glob patterns.
        valid_file_extension: file extension to include (e.g., ".txt").
        exclude_pattern: Regex pattern to exclude files (e.g., r"\.tmp$", r"temp.*").
        recursive: Whether to traverse subdirectories recursively.

    Returns:
        List of Path objects for matching files.
    """
    matched_files: List[Path] = []
    exclude_regex = re.compile(exclude_pattern) if exclude_pattern else None

    for pattern in paths:
        # Use pathlib's glob to handle patterns; set recursive flag appropriately
        for p in Path(pattern).glob("*") if not recursive else Path(pattern).rglob("*"):
            if not p.is_file():
                continue
            if p.suffix != valid_file_extension:
                continue
            if exclude_regex and exclude_regex.search(p.name):
                continue
            matched_files.append(p)

    return matched_files