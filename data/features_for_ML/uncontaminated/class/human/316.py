from cosmos_xenna._cosmos_xenna.file_distribution import models as rust_models

class ByteRange:
    """Represents a range of bytes within a file.

    Attributes:
        start: Starting byte position (inclusive)
        end: Ending byte position (exclusive)
    """

    start: int
    end: int

    def to_rust(self) -> rust_models.ByteRange:
        return rust_models.ByteRange(start=self.start, end=self.end)