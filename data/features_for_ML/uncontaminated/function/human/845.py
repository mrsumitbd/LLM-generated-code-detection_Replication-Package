from importlib.metadata import PackageNotFoundError, version

def get_version() -> str:
    """Get version from package metadata

    Returns:
        str: Current version
    """
    try:
        return version("rovr")
    except PackageNotFoundError:
        return "master"