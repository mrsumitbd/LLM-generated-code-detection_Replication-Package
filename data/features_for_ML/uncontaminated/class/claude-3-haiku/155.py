class DocumentConverterResult:
    """The result of converting a document to text."""

    def __init__(self, title: str | None = None, text_content: str = ""):
        self.title = title
        self.text_content = text_content

    def __str__(self):
        if self.title:
            return f"{self.title}\n{self.text_content}"
        else:
            return self.text_content

    def __len__(self):
        return len(self.text_content)

    def __bool__(self):
        return bool(self.text_content)