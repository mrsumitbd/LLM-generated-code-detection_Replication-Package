def has_scope(request: Request, scope: str) -> bool:
    """Check if current user has a specific scope.

    Args:
        request: FastAPI request object
        scope: Scope to check

    Returns:
        bool: True if user has the scope
    """
    token = request.scope.get("user", {})
    scopes = token.get("scopes", [])
    return scope in scopes