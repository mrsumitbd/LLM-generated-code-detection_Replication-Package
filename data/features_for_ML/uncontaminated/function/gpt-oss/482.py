import re
from typing import Tuple

# Regular expression for semantic versioning (semver 2.0.0)
_SEMVER_RE = re.compile(
    r"""
    ^[vV]?                                   # optional leading 'v' or 'V'
    (?P<major>0|[1-9]\d*)\.                  # major
    (?P<minor>0|[1-9]\d*)\.                  # minor
    (?P<patch>0|[1-9]\d*)                    # patch
    (?:-(?P<prerelease>[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?  # optional prerelease
    (?:\+(?P<build>[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?      # optional build
    $                                         # end of string
    """,
    re.VERBOSE,
)

def validate_version(version: str) -> Tuple[bool, str, bool]:
    """
    Validate version format and determine if it's stable or pre-release.

    Parameters
    ----------
    version : str
        The version string to validate.

    Returns
    -------
    Tuple[bool, str, bool]
        (is_valid, clean_version, is_stable)

        * is_valid   : True if the version string matches the semantic
                       versioning pattern.
        * clean_version : The version string stripped of any leading 'v'/'V',
                          whitespace, and build metadata (the part after '+').
                          If the version is invalid, this is an empty string.
        * is_stable : True if the version has no pre‑release part (i.e. no
                       '-' component). If the version is invalid, this is
                       False.
    """
    if not isinstance(version, str):
        return False, "", False

    version = version.strip()
    match = _SEMVER_RE.match(version)
    if not match:
        return False, "", False

    # Remove leading 'v' or 'V' if present
    clean = version.lstrip("vV").strip()

    # Strip build metadata (the part after '+')
    if "+" in clean:
        clean = clean.split("+", 1)[0]

    # Determine stability
    is_stable = "-" not in clean

    return True, clean, is_stable