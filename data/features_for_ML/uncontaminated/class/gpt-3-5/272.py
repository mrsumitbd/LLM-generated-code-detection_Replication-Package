class OneLakeFileContent:

    def __init__(self, properties: dict, content: bytes) -> None:
        self.properties = properties
        self.content = content

    def get_properties(self) -> dict:
        return self.properties

    def get_content(self) -> bytes:
        return self.content

    def get_content_length(self) -> int:
        return len(self.content)

    def get_content_type(self) -> str:
        return self.properties.get('Content-Type', '')

    def get_content_encoding(self) -> str:
        return self.properties.get('Content-Encoding', '')