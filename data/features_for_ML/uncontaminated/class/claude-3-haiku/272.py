class OneLakeFileContent:
    def __init__(self, properties: dict, content: bytes) -> None:
        self._properties = properties
        self._content = content

    def get_properties(self) -> dict:
        return self._properties

    def get_content(self) -> bytes:
        return self._content

    def get_content_length(self) -> int:
        return len(self._content)

    def get_content_type(self) -> str:
        return self._properties.get('content-type', '')

    def get_content_encoding(self) -> str:
        return self._properties.get('content-encoding', '')