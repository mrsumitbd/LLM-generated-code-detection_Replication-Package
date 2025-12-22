def get_arch(system: PLATFORM) -> str:
    if system == PLATFORM.WINDOWS:
        return "x86_64"
    elif system == PLATFORM.LINUX:
        return "x86_64"
    elif system == PLATFORM.MACOS:
        return "x86_64"
    else:
        return "Unknown"