from typing import Tuple
import re

def validate_version(version: str) -> Tuple[bool, str, bool]:
    """
    Validate version format and determine if it's stable or pre-release.

    Returns:
        (is_valid, clean_version, is_stable)
    """
    if not version or not isinstance(version, str):
        return (False, "", False)
    
    # Strip whitespace
    version = version.strip()
    
    if not version:
        return (False, "", False)
    
    # Remove leading 'v' if present
    clean_version = version.lstrip('v')
    
    # Pattern for semantic versioning: major.minor.patch with optional pre-release and metadata
    # Pre-release identifiers: alpha, beta, rc, a, b, dev, etc.
    # Stable versions: only major.minor.patch (with optional patch)
    pattern = r'^(\d+)(?:\.(\d+))?(?:\.(\d+))?(?:[-.]?(alpha|beta|rc|a|b|dev|pre|preview|c)(?:\.?\d+)?)?(?:\+[a-zA-Z0-9.-]+)?$'
    
    match = re.match(pattern, clean_version, re.IGNORECASE)
    
    if not match:
        return (False, "", False)
    
    # Check if it's a pre-release version
    pre_release_keywords = ('alpha', 'beta', 'rc', 'a', 'b', 'dev', 'pre', 'preview', 'c')
    is_stable = not any(keyword in clean_version.lower() for keyword in pre_release_keywords)
    
    return (True, clean_version, is_stable)