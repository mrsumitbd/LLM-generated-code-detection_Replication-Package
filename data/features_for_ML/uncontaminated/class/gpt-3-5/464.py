class SaveDocumentOutput:
    """Output of the save_docling_document tool."""
    
    def __init__(self, success, message):
        self.success = success
        self.message = message
        
    def __str__(self):
        return f"Success: {self.success}, Message: {self.message}"