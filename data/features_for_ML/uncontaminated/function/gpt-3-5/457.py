def extract_simple(file_path: str, mime_type: str | None = None, response_format: Literal["text", "markdown"] = "text") -> str:
    import magic
    import markdown

    def read_file(file_path):
        with open(file_path, 'r') as file:
            return file.read()

    def extract_text(file_path):
        return read_file(file_path)

    def extract_markdown(file_path):
        text = read_file(file_path)
        return markdown.markdown(text)

    if mime_type is not None:
        mime = magic.Magic(mime=True)
        detected_mime = mime.from_file(file_path)
        if detected_mime != mime_type:
            return f"Error: File MIME type '{detected_mime}' does not match expected MIME type '{mime_type}'."

    if response_format == "text":
        return extract_text(file_path)
    elif response_format == "markdown":
        return extract_markdown(file_path)