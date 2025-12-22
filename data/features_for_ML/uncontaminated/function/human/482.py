import re
from typing import Tuple

def validate_version(version: str) -> Tuple[bool, str, bool]:
    """
    Validate version format and determine if it's stable or pre-release.

    Returns:
        (is_valid, clean_version, is_stable)
    """
    # Remove 'v' prefix if present
    clean_version = version.lstrip('v')

    # Semantic version pattern
    stable_pattern = r'^(\d+)\.(\d+)\.(\d+)$'
    prerelease_pattern = r'^(\d+)\.(\d+)\.(\d+)-(.+)$'

    if re.match(stable_pattern, clean_version):
        return True, clean_version, True
    elif re.match(prerelease_pattern, clean_version):
        return True, clean_version, False
    else:
        return False, clean_version, False