import os
from typing import Iterable, Optional, Union


class Output:
    """Output file."""

    def __init__(
        self,
        path: Union[str, os.PathLike],
        mode: str = "w",
        encoding: Optional[str] = "utf-8",
        buffering: int = -1,
    ) -> None:
        """
        Open a file for writing.

        Parameters
        ----------
        path : str or PathLike
            Path to the output file.
        mode : str, optional
            File mode. Defaults to "w".
        encoding : str, optional
            Text encoding. Ignored if mode is binary. Defaults to "utf-8".
        buffering : int, optional
            Buffering policy. Defaults to -1 (system default).
        """
        self.path = os.fspath(path)
        self.mode = mode
        self.encoding = encoding
        self.buffering = buffering
        self._file = open(self.path, mode, encoding=encoding, buffering=buffering)

    # ------------------------------------------------------------------
    # Basic file operations
    # ------------------------------------------------------------------
    def write(self, data: str) -> int:
        """Write a string to the file."""
        return self._file.write(data)

    def writelines(self, lines: Iterable[str]) -> None:
        """Write a sequence of strings to the file."""
        self._file.writelines(lines)

    def flush(self) -> None:
        """Flush the write buffer."""
        self._file.flush()

    def close(self) -> None:
        """Close the file."""
        if not self._file.closed:
            self._file.close()

    # ------------------------------------------------------------------
    # Context manager support
    # ------------------------------------------------------------------
    def __enter__(self) -> "Output":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    # ------------------------------------------------------------------
    # Convenience methods
    # ------------------------------------------------------------------
    def __iter__(self):
        """Iterate over the file's lines (read mode only)."""
        return iter(self._file)

    def __repr__(self) -> str:
        return f"<Output path={self.path!r} mode={self.mode!r}>"

    def __del__(self) -> None:
        """Ensure the file is closed when the object is garbage‑collected."""
        self.close()