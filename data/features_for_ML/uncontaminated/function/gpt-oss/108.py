import re
from pathlib import Path
from typing import Tuple

def update_cargo_toml(file_path: Path, version: str) -> Tuple[bool, str, str]:
    """
    Update a Cargo.toml file that has a hardcoded version (not using workspace).

    Returns:
        (changed, old_version, new_version)
    """
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    content = file_path.read_text(encoding="utf-8")
    # Regex to match a line like: version = "0.1.0" or version = '0.1.0'
    pattern = re.compile(r'^(?P<indent>\s*version\s*=\s*)(?P<quote>["\'])(?P<ver>[^"\']*)(?P=quote)', re.MULTILINE)

    match = pattern.search(content)
    if not match:
        # No version line found
        return False, "", version

    old_version = match.group("ver")
    if old_version == version:
        return False, old_version, version

    # Replace the old version with the new one
    new_line = f'{match.group("indent")}{match.group("quote")}{version}{match.group("quote")}'
    new_content = pattern.sub(new_line, content, count=1)

    file_path.write_text(new_content, encoding="utf-8")
    return True, old_version, version