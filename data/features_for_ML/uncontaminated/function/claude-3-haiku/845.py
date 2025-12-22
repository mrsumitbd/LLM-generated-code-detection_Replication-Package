import importlib.metadata

def get_version() -> str:
    """Get version from package metadata

    Returns:
        str: Current version
    """
    try:
        return importlib.metadata.version(__package__)
    except importlib.metadata.PackageNotFoundError:
        return "0.0.0"