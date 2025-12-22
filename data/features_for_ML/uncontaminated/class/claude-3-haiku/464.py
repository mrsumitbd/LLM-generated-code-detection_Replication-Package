class SaveDocumentOutput:
    """Output of the save_docling_document tool."""

    def __init__(self, document_id, document_path, success, error_message=None):
        self.document_id = document_id
        self.document_path = document_path
        self.success = success
        self.error_message = error_message

    def __str__(self):
        if self.success:
            return f"Saved document {self.document_id} to {self.document_path}"
        else:
            return f"Failed to save document {self.document_id}: {self.error_message}"

    def __repr__(self):
        return f"SaveDocumentOutput(document_id={self.document_id}, document_path='{self.document_path}', success={self.success}, error_message={self.error_message})"