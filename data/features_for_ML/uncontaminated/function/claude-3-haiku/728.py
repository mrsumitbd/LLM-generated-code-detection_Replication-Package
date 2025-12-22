def _check_link_requires_python(
    link: Link,
    version_info: Tuple[int, int, int],
    ignore_requires_python: bool = False,
) -> bool:
    requires_python = link.requires_python
    if requires_python is None or ignore_requires_python:
        return True

    try:
        specifier = SpecifierSet(requires_python)
        return version_info in specifier
    except InvalidSpecifier:
        return False