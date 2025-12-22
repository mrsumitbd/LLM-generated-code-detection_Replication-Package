class OneLakeFileContent:

    def __init__(self, properties: dict, content: bytes) -> None:
        self._properties = properties if properties is not None else {}
        self._content = content if content is not None else b""

    def get_properties(self) -> dict:
        return self._properties

    def get_content(self) -> bytes:
        return self._content

    def get_content_length(self) -> int:
        return len(self._content)

    def get_content_type(self) -> str:
        return self._properties.get("content_type", "")

    def get_content_encoding(self) -> str:
        return self._properties.get("content_encoding", "")