def has_scope(request: Request, scope: str) -> bool:
    if request.user is None:
        return False
    return scope in request.user.scopes