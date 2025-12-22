def _collect_document_permissions(document: Document) -> list[str]:
    permissions = []
    for user in document.users:
        permissions.extend(user.permissions)
    return permissions