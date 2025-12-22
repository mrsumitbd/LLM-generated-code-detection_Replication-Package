from typing import TYPE_CHECKING, FrozenSet, Iterable, List, Optional, Set, Tuple, Union
from pipask._vendor.pip._internal.models.link import Link
from pipask._vendor.pip._internal.utils.packaging import check_requires_python
from packaging import specifiers

def _check_link_requires_python(
    link: Link,
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
    try:
        is_compatible = check_requires_python(
            link.requires_python,
            version_info=version_info,
        )
    except specifiers.InvalidSpecifier:
        logger.debug(
            "Ignoring invalid Requires-Python (%r) for link: %s",
            link.requires_python,
            link,
        )
    else:
        if not is_compatible:
            version = ".".join(map(str, version_info))
            if not ignore_requires_python:
                logger.verbose(
                    "Link requires a different Python (%s not in: %r): %s",
                    version,
                    link.requires_python,
                    link,
                )
                return False

            logger.debug(
                "Ignoring failed Requires-Python check (%s not in: %r) for link: %s",
                version,
                link.requires_python,
                link,
            )

    return True