def _collect_document_permissions(document: Document) -> list[str]:
    permissions = []
    for permission in document.permissions:
        permissions.append(permission.name)
    return permissions