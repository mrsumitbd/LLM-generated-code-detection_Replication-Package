import platform

def get_machine_format() -> str:
    """
    Returns the machine format (architecture) of the current system.
    
    Returns:
        str: The machine format (e.g., 'x86_64', 'arm64', 'i386', etc.)
    """
    return platform.machine()