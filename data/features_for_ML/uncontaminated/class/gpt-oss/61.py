from __future__ import annotations

import os
from collections import OrderedDict
from pathlib import Path
from typing import Optional

# Try to import chardet for better detection; fall back to a simple heuristic if unavailable.
try:
    import chardet  # type: ignore
except Exception:  # pragma: no cover
    chardet = None


class EncodingManager:
    """Manages file encodings across multiple operations to ensure consistency."""

    def __init__(self, max_cache_size: Optional[int] = None) -> None:
        """
        Initialize the EncodingManager.

        Parameters
        ----------
        max_cache_size : int | None
            Maximum number of path/encoding pairs to keep in the cache.
            If None, the cache is unbounded.
        """
        self._max_cache_size = max_cache_size
        self._cache: OrderedDict[Path, str] = OrderedDict()

    def detect_encoding(self, path: Path) -> str:
        """
        Detect the encoding of a file.

        Parameters
        ----------
        path : Path
            Path to the file whose encoding should be detected.

        Returns
        -------
        str
            The name of the detected encoding.

        Raises
        ------
        FileNotFoundError
            If the file does not exist.
        PermissionError
            If the file cannot be read.
        """
        if not path.is_file():
            raise FileNotFoundError(f"No such file: {path}")

        # Read a chunk of the file for detection
        try:
            with path.open("rb") as f:
                sample = f.read(8192)
        except PermissionError as exc:
            raise PermissionError(f"Permission denied: {path}") from exc

        # Use chardet if available
        if chardet is not None:
            result = chardet.detect(sample)
            encoding = result.get("encoding")
            confidence = result.get("confidence", 0.0)
            if encoding and confidence >= 0.5:
                return encoding

        # Fallback heuristic: try utf-8, then latin-1
        try:
            sample.decode("utf-8")
            return "utf-8"
        except UnicodeDecodeError:
            pass

        # If utf-8 fails, assume latin-1 (covers most single-byte encodings)
        return "latin-1"

    def get_encoding(self, path: Path) -> str:
        """
        Retrieve the encoding for a file, using the cache if possible.

        Parameters
        ----------
        path : Path
            Path to the file.

        Returns
        -------
        str
            The encoding of the file.
        """
        # Resolve to an absolute path to avoid duplicate entries for the same file
        abs_path = path.resolve()

        # Check cache
        if abs_path in self._cache:
            # Move to end to mark as recently used
            self._cache.move_to_end(abs_path)
            return self._cache[abs_path]

        # Detect encoding and cache it
        encoding = self.detect_encoding(abs_path)
        self._cache[abs_path] = encoding

        # Enforce cache size limit
        if self._max_cache_size is not None and len(self._cache) > self._max_cache_size:
            # Pop the least recently used item
            self._cache.popitem(last=False)

        return encoding