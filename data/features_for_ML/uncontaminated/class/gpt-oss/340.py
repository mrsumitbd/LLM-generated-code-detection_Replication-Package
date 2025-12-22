class Encoder:
    def __init__(self, encoding: str = "utf-8"):
        self.encoding = encoding

    def encode(self, data: str) -> bytes:
        if not isinstance(data, str):
            raise TypeError("data must be a string")
        return data.encode(self.encoding)

    def decode(self, data: bytes) -> str:
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("data must be bytes")
        return data.decode(self.encoding)

    def __repr__(self) -> str:
        return f"<Encoder encoding={self.encoding!r}>"