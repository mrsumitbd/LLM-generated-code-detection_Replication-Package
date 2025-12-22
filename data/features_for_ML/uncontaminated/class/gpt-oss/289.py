from __future__ import annotations

import datetime
import re
from dataclasses import dataclass, field
from typing import Union


@dataclass
class TableInfo:
    name: str
    size: Union[int, str]  # bytes or human‑readable string
    last_updated: datetime.datetime | None = None

    # ------------------------------------------------------------------
    # Post‑initialisation
    # ------------------------------------------------------------------
    def __post_init__(self) -> None:
        """Ensure that `size` is stored as an integer number of bytes."""
        if isinstance(self.size, str):
            self.size = self.parse_size_string(self.size)
        if not isinstance(self.size, int):
            raise TypeError("size must be an int or a size string")
        if self.last_updated is None:
            self.last_updated = datetime.datetime.now(tz=datetime.timezone.utc)

    # ------------------------------------------------------------------
    # Size parsing
    # ------------------------------------------------------------------
    @staticmethod
    def parse_size_string(size_str: str) -> int:
        """
        Convert a human‑readable size string into an integer number of bytes.
        Supported suffixes: B, K, KB, M, MB, G, GB, T, TB (case‑insensitive).
        """
        size_str = size_str.strip().upper()
        match = re.fullmatch(r"(\d+(?:\.\d+)?)([KMGTP]?B?)", size_str)
        if not match:
            raise ValueError(f"Invalid size string: {size_str!r}")

        number, unit = match.groups()
        number = float(number)

        multiplier = {
            "B": 1,
            "": 1,
            "K": 1024,
            "KB": 1024,
            "M": 1024**2,
            "MB": 1024**2,
            "G": 1024**3,
            "GB": 1024**3,
            "T": 1024**4,
            "TB": 1024**4,
            "P": 1024**5,
            "PB": 1024**5,
        }.get(unit, None)

        if multiplier is None:
            raise ValueError(f"Unknown unit in size string: {unit!r}")

        return int(number * multiplier)

    # ------------------------------------------------------------------
    # Table characteristics
    # ------------------------------------------------------------------
    def is_large_table(self) -> bool:
        """
        Return True if the table size exceeds 100 MiB.
        """
        return self.size > 100 * 1024**2

    def priority_score(self) -> float:
        """
        Compute a priority score based on size and age.
        Larger and newer tables get higher scores.
        Formula: size_bytes / (age_seconds + 1)
        """
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        age = (now - self.last_updated).total_seconds()
        return self.size / (age + 1)

    def is_expired(self, expire_seconds: int = 120) -> bool:
        """
        Return True if the table has not been updated within the given
        number of seconds.
        """
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        age = (now - self.last_updated).total_seconds()
        return age > expire_seconds