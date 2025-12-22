def _collect_document_permissions(document: "Document") -> list[str]:
    """
    Collects a list of permission names from a `Document` instance.

    The function attempts to retrieve permissions in a flexible manner,
    supporting a variety of common APIs that a Document object might expose.
    """
    permissions: list[str] = []

    # 1. Direct attribute access
    if hasattr(document, "permissions"):
        perm_attr = getattr(document, "permissions")
        if isinstance(perm_attr, (list, tuple, set)):
            permissions = [str(p) for p in perm_attr]
        elif isinstance(perm_attr, dict):
            # If the dict maps permission names to booleans, include only those that are True
            permissions = [k for k, v in perm_attr.items() if v]
        else:
            # Fallback: treat the attribute as a single permission value
            permissions = [str(perm_attr)]

    # 2. Method-based access
    elif hasattr(document, "get_permissions"):
        try:
            perms = document.get_permissions()
            if isinstance(perms, (list, tuple, set)):
                permissions = [str(p) for p in perms]
            elif isinstance(perms, dict):
                permissions = [k for k, v in perms.items() if v]
            else:
                permissions = [str(perms)]
        except Exception:
            permissions = []

    # 3. Alternative method name
    elif hasattr(document, "getDocumentPermissions"):
        try:
            perms = document.getDocumentPermissions()
            if isinstance(perms, (list, tuple, set)):
                permissions = [str(p) for p in perms]
            elif isinstance(perms, dict):
                permissions = [k for k, v in perms.items() if v]
            else:
                permissions = [str(perms)]
        except Exception:
            permissions = []

    # Ensure the result is a list of strings
    return [str(p) for p in permissions]