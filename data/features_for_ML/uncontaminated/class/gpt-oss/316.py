from __future__ import annotations

import rust_models


class ByteRange:
    """Represents a range of bytes within a file.

    Attributes:
        start: Starting byte position (inclusive)
        end: Ending byte position (exclusive)
    """

    __slots__ = ("start", "end")

    def __init__(self, start: int, end: int):
        if not isinstance(start, int) or not isinstance(end, int):
            raise TypeError("start and end must be integers")
        if start < 0 or end < 0:
            raise ValueError("start and end must be non‑negative")
        if start > end:
            raise ValueError("start must be less than or equal to end")
        self.start = start
        self.end = end

    def to_rust(self) -> rust_models.ByteRange:
        """Convert to the corresponding Rust model."""
        return rust_models.ByteRange(start=self.start, end=self.end)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(start={self.start}, end={self.end})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ByteRange):
            return NotImplemented
        return self.start == other.start and self.end == other.end

    def __hash__(self) -> int:
        return hash((self.start, self.end))