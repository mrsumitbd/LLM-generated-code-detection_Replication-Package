from playa.document import Document

def _collect_document_permissions(document: Document) -> list[str]:
    permissions = []
    if document.is_printable:
        permissions.append("printable")
    if document.is_modifiable:
        permissions.append("modifiable")
    if document.is_extractable:
        permissions.append("extractable")
    return permissions