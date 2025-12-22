def get_global_security_manager() -> SecurityManager:
    """Get the global security manager instance.

    Returns:
        SecurityManager: The global security manager

    Raises:
        RuntimeError: If security manager has not been initialized
    """
    global _global_security_manager
    if _global_security_manager is None:
        raise RuntimeError("Security manager has not been initialized")
    return _global_security_manager