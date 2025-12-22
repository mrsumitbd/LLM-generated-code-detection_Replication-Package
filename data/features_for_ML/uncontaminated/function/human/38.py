from .manager import SecurityManager

def get_global_security_manager() -> SecurityManager:
    """Get the global security manager instance.

    Returns:
        SecurityManager: The global security manager

    Raises:
        RuntimeError: If security manager has not been initialized
    """
    if _security_manager is None:
        raise RuntimeError(
            "Security manager not initialized. Call create_security_manager() during application startup."
        )
    return _security_manager