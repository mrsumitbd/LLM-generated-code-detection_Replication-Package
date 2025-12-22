def _collect_document_permissions(document: Document) -> list[str]:
    permissions = []
    
    if hasattr(document, 'permissions') and document.permissions:
        if isinstance(document.permissions, list):
            permissions.extend(document.permissions)
        elif isinstance(document.permissions, str):
            permissions.append(document.permissions)
    
    return permissions