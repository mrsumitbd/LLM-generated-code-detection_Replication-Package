def is_supported(cls) -> bool:
    import platform
    return platform.system() == 'Darwin'