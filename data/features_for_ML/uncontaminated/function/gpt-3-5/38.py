def get_global_security_manager() -> SecurityManager:
    global security_manager
    if security_manager is None:
        raise RuntimeError("Security manager has not been initialized")
    return security_manager