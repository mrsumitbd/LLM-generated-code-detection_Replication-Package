from fastapi import Request

def has_scope(request: Request, scope: str) -> bool:
    """
    Check if current user has a specific scope.

    Args:
        request: FastAPI request object
        scope: Scope to check

    Returns:
        bool: True if user has the scope
    """
    # Try to get the user object from request.state
    user = getattr(request.state, "user", None)
    if not user:
        return False

    # The user object may expose scopes in different ways:
    # 1. As a list/tuple of strings: user.scopes
    # 2. As a space‑separated string: user.scopes
    # 3. As a dict with a 'scopes' key: user.scopes
    # 4. As a property that returns a list: user.scopes
    # 5. As a property that returns a string: user.scopes

    # First, try to get the scopes attribute
    scopes_attr = getattr(user, "scopes", None)
    if scopes_attr is None:
        return False

    # Normalize scopes to a set of strings
    if isinstance(scopes_attr, (list, tuple, set)):
        scopes = set(scopes_attr)
    elif isinstance(scopes_attr, str):
        # Split on whitespace
        scopes = set(scopes_attr.split())
    elif isinstance(scopes_attr, dict):
        # If dict, look for a 'scopes' key
        scopes = set(scopes_attr.get("scopes", []))
    else:
        # Unsupported type
        return False

    return scope in scopes