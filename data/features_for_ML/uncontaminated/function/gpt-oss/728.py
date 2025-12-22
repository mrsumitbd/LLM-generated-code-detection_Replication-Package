from typing import Tuple
from packaging.specifiers import SpecifierSet
from packaging.version import Version

def _check_link_requires_python(
    link,
    version_info: Tuple[int, int, int],
    ignore_requires_python: bool = False,
) -> bool:
    """
    Return whether the given Python version is compatible with a link's
    "Requires-Python" value.

    :param version_info: A 3-tuple of ints representing the Python
        major-minor-micro version to check.
    :param ignore_requires_python: Whether to ignore the "Requires-Python"
        value if the given Python version isn't compatible.
    """
    # If the link has no requires_python metadata, it's compatible by default.
    requires_python = getattr(link, "requires_python", None)
    if not requires_python:
        return True

    # Convert the version tuple to a Version object.
    py_version = Version(f"{version_info[0]}.{version_info[1]}.{version_info[2]}")

    try:
        spec_set = SpecifierSet(requires_python)
    except Exception:
        # If the specifier string is malformed, treat it as compatible.
        return True

    if py_version in spec_set:
        return True

    # If the version is not compatible, respect the ignore flag.
    return ignore_requires_python