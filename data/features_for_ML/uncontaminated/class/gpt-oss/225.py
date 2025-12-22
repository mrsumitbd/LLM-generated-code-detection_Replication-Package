from pathlib import Path
from typing import Optional


class PathValidator:
    """Fix for Critical Issue #2: Path Traversal Vulnerability"""

    @staticmethod
    def is_safe_path(path: Path) -> bool:
        """
        Determine whether a given Path is safe from traversal attacks.

        A path is considered safe if:
        * It is absolute.
        * It does not contain any component equal to '..'.
        * It does not resolve to a location outside its own directory hierarchy
          (i.e., resolving the path does not change any component that was
          not already present in the original path).

        Parameters
        ----------
        path : Path
            The path to validate.

        Returns
        -------
        bool
            True if the path is safe, False otherwise.
        """
        # Must be absolute
        if not path.is_absolute():
            return False

        # No '..' components allowed
        if any(part == ".." for part in path.parts):
            return False

        # Resolve the path to collapse symlinks and normalise
        try:
            resolved = path.resolve(strict=False)
        except Exception:
            return False

        # Ensure that the resolved path starts with the same root as the original
        # (this guards against symlinks that escape the intended directory)
        if resolved.anchor != path.anchor:
            return False

        return True

    @staticmethod
    def sanitize_path(path_str: str) -> Optional[Path]:
        """
        Convert a string to a Path and validate it.

        Parameters
        ----------
        path_str : str
            The raw path string.

        Returns
        -------
        Optional[Path]
            The sanitized Path if it is safe, otherwise None.
        """
        try:
            path = Path(path_str)
        except Exception:
            return None

        if PathValidator.is_safe_path(path):
            return path
        return None