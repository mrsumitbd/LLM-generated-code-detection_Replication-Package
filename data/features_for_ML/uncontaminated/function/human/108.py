import re
from pathlib import Path

def update_cargo_toml(file_path: Path, version: str) -> tuple[bool, str, str]:
    """
    Update a Cargo.toml file that has hardcoded version (not using workspace).

    Returns: (changed, old_version, new_version)
    """
    content = file_path.read_text()
    match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
    old_version = match.group(1) if match else "NOT FOUND"

    if old_version == version:
        return False, old_version, version

    # Update the version field
    new_content = re.sub(r'^(version\s*=\s*)"[^"]+"', rf'\1"{version}"', content, count=1, flags=re.MULTILINE)

    file_path.write_text(new_content)
    return True, old_version, version