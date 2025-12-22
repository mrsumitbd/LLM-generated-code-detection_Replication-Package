class ByteRange:
    """Represents a range of bytes within a file.

    Attributes:
        start: Starting byte position (inclusive)
        end: Ending byte position (exclusive)
    """

    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def __str__(self):
        return f"ByteRange(start={self.start}, end={self.end})"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, ByteRange):
            return self.start == other.start and self.end == other.end
        return False

    def __hash__(self):
        return hash((self.start, self.end))

    def to_rust(self) -> rust_models.ByteRange:
        return rust_models.ByteRange(start=self.start, end=self.end)