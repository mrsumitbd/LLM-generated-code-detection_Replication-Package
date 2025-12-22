# Assume that the global security manager is stored in a module-level variable
# named `_global_security_manager`.  The `SecurityManager` type is imported
# from the appropriate module.

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Import for type checking only; the actual import may be elsewhere.
    from .security_manager import SecurityManager  # Adjust the import path as needed

# The global instance (initially None until initialized elsewhere)
_global_security_manager = None  # type: SecurityManager | None


def get_global_security_manager() -> "SecurityManager":
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