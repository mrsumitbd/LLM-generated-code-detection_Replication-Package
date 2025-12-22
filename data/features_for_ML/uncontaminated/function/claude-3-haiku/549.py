import platform

def get_arch(system: PLATFORM) -> str:
    """
    Returns the architecture of the given system.

    Args:
        system (PLATFORM): The platform for which the architecture is to be determined.

    Returns:
        str: The architecture of the given system.
    """
    if system == PLATFORM.WINDOWS:
        return platform.machine()
    elif system == PLATFORM.LINUX:
        return platform.machine()
    elif system == PLATFORM.MACOS:
        return platform.machine()
    else:
        return "Unknown"