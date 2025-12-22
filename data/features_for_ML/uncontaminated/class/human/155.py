
class DocumentConverterResult:
    """The result of converting a document to text."""

    def __init__(self, title: str | None = None, text_content: str = ""):
        self.title: str | None = title
        self.text_content: str = text_content