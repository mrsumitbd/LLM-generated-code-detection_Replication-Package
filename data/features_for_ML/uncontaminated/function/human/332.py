from fastapi import HTTPException, Request

def has_scope(request: Request, scope: str) -> bool:
    """Check if current user has a specific scope.

    Args:
        request: FastAPI request object
        scope: Scope to check

    Returns:
        bool: True if user has the scope
    """
    auth_result = get_auth_result(request)
    return scope in auth_result.scopes if auth_result else False