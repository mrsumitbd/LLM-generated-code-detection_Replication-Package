def has_scope(request: Request, scope: str) -> bool:
    """Check if current user has a specific scope.

    Args:
        request: FastAPI request object
        scope: Scope to check

    Returns:
        bool: True if user has the scope
    """
    if "user" not in request.state:
        return False

    user = request.state.user
    if "scopes" not in user:
        return False

    return scope in user.scopes