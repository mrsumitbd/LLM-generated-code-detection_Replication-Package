import threading

_security_manager = None
_security_manager_lock = threading.Lock()

def get_global_security_manager() -> SecurityManager:
    """Get the global security manager instance.

    Returns:
        SecurityManager: The global security manager

    Raises:
        RuntimeError: If security manager has not been initialized
    """
    global _security_manager
    with _security_manager_lock:
        if _security_manager is None:
            raise RuntimeError("Security manager has not been initialized")
        return _security_manager