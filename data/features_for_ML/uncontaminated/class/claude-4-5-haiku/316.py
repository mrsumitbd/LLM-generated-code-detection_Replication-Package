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

    def __repr__(self) -> str:
        return f"ByteRange(start={self.start}, end={self.end})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, ByteRange):
            return False
        return self.start == other.start and self.end == other.end

    def __hash__(self) -> int:
        return hash((self.start, self.end))

    def __len__(self) -> int:
        return self.end - self.start