import pathlib
import warnings
from typing import Iterable


def _warn_if_mismatch(old: pathlib.Path, new: pathlib.Path, *, key: str) -> bool:
    """
    Compare two files and emit a warning if they differ.

    Parameters
    ----------
    old : pathlib.Path
        Path to the original file.
    new : pathlib.Path
        Path to the new file.
    key : str
        Identifier used in the warning message.

    Returns
    -------
    bool
        True if a mismatch was detected (or one of the files is missing),
        False otherwise.
    """
    # Helper to read file contents safely
    def _read(path: pathlib.Path) -> bytes | None:
        try:
            return path.read_bytes()
        except FileNotFoundError:
            return None
        except OSError as exc:
            warnings.warn(
                f"Could not read file for key '{key}': {path!s} ({exc})",
                RuntimeWarning,
            )
            return None

    old_bytes = _read(old)
    new_bytes = _read(new)

    # If either file is missing, warn and consider it a mismatch
    if old_bytes is None or new_bytes is None:
        missing = []
        if old_bytes is None:
            missing.append(f"old file missing: {old!s}")
        if new_bytes is None:
            missing.append(f"new file missing: {new!s}")
        warnings.warn(
            f"Mismatch for key '{key}': {', '.join(missing)}",
            RuntimeWarning,
        )
        return True

    # Compare contents
    if old_bytes != new_bytes:
        warnings.warn(
            f"Mismatch for key '{key}': {old!s} != {new!s}",
            RuntimeWarning,
        )
        return True

    return False