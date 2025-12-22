def is_supported(cls) -> bool:
    """
    Check if the current system supports seatbelt sandboxing.
    
    Returns:
        True if the system supports seatbelt (macOS), False otherwise
    """
    import platform
    return platform.system() == "Darwin"