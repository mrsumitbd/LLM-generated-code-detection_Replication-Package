import rust_models

class ByteRange:
    """Represents a range of bytes within a file.

    Attributes:
        start: Starting byte position (inclusive)
        end: Ending byte position (exclusive)
    """

    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def to_rust(self) -> rust_models.ByteRange:
        return rust_models.ByteRange(start=self.start, end=self.end)