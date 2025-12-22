class SaveDocumentOutput:
    """Output of the save_docling_document tool."""
    
    def __init__(self, success: bool, message: str, file_path: str = None):
        """
        Initialize SaveDocumentOutput.
        
        Args:
            success: Whether the save operation was successful
            message: A message describing the result of the operation
            file_path: The path where the document was saved (if successful)
        """
        self.success = success
        self.message = message
        self.file_path = file_path
    
    def __repr__(self) -> str:
        """Return string representation of SaveDocumentOutput."""
        return f"SaveDocumentOutput(success={self.success}, message='{self.message}', file_path='{self.file_path}')"
    
    def __str__(self) -> str:
        """Return human-readable string representation."""
        if self.success:
            return f"Successfully saved document to {self.file_path}"
        else:
            return f"Failed to save document: {self.message}"