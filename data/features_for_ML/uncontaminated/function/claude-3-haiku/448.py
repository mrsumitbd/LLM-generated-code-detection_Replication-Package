import sys
import platform

def is_supported(cls) -> bool:
    """
    Check if the current system supports seatbelt sandboxing.
    
    Returns:
        True if the system supports seatbelt (macOS), False otherwise
    """
    return sys.platform == 'darwin' and platform.mac_ver()[0] >= '10.15'