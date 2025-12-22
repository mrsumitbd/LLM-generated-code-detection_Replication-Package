def _check_link_requires_python(
    link: Link,
    version_info: Tuple[int, int, int],
    ignore_requires_python: bool = False,
) -> bool:
    if ignore_requires_python:
        return True
    requires_python = link.requires_python
    if not requires_python:
        return True
    requires_python_spec = packaging.specifiers.SpecifierSet(requires_python)
    python_version = ".".join(str(part) for part in version_info)
    return python_version in requires_python_spec