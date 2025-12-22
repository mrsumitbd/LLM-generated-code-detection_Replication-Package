class DocumentConverterResult:
    """The result of converting a document to text."""

    def __init__(self, title: str | None = None, text_content: str = ""):
        self.title = title
        self.text_content = text_content

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(title={self.title!r}, text_content={self.text_content!r})"

    def __str__(self) -> str:
        return self.text_content or ""