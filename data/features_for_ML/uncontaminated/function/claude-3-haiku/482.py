import re

def validate_version(version: str) -> Tuple[bool, str, bool]:
    """
    Validate version format and determine if it's stable or pre-release.

    Returns:
        (is_valid, clean_version, is_stable)
    """
    version_pattern = r'^(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*))?$'
    match = re.match(version_pattern, version)

    if not match:
        return False, version, False

    major, minor, patch, pre_release = match.groups()
    major, minor, patch = int(major), int(minor), int(patch)
    is_stable = pre_release is None

    clean_version = f"{major}.{minor}.{patch}"
    return True, clean_version, is_stable