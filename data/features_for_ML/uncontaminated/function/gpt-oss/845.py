def get_version() -> str:
    """Get version from package metadata

    Returns:
        str: Current version
    """
    # Try to import the modern importlib.metadata API
    try:
        from importlib.metadata import version, PackageNotFoundError
    except ImportError:  # pragma: no cover
        # Fallback for older Python versions
        from importlib_metadata import version, PackageNotFoundError

    # Determine the package name to query
    pkg_name = __package__ or __name__
    try:
        return version(pkg_name)
    except PackageNotFoundError:
        # If the metadata is not available, return a default placeholder
        return "0.0.0"