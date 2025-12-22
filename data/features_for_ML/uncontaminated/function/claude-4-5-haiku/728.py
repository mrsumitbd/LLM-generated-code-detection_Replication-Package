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
    if ignore_requires_python:
        return True
    
    requires_python = link.requires_python
    if requires_python is None:
        return True
    
    try:
        from packaging.specifiers import SpecifierSet
        spec = SpecifierSet(requires_python)
        version_string = ".".join(str(v) for v in version_info)
        return version_string in spec
    except Exception:
        return True