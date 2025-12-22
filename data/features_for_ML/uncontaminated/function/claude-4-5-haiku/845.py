def get_version() -> str:
    """Get version from package metadata

    Returns:
        str: Current version
    """
    try:
        from importlib.metadata import version
        return version("anthropic")
    except Exception:
        return "unknown"