class DocumentConverterResult:
    """The result of converting a document to text."""

    def __init__(self, title: str | None = None, text_content: str = ""):
        self.title = title
        self.text_content = text_content