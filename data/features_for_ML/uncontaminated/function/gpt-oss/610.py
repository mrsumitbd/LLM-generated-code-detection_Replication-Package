import platform

def get_machine_format() -> str:
    """
    Return a string describing the machine architecture.
    """
    return platform.machine()