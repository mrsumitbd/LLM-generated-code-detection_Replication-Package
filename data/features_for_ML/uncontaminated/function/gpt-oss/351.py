from pathlib import Path
from typing import Optional

def code_as_text(att: "Attachment") -> "Attachment":
    """
    Processes any file as plain text for code analysis, skipping binaries.
    If a directory is given, it delegates to the appropriate repository loader.
    """
    # Resolve the path
    path = Path(att.path)

    # If the attachment is a directory, delegate to the repository loader
    if path.is_dir():
        try:
            # Import lazily to avoid circular imports
            from .repo_loader import load_repository
        except Exception:
            # If the loader cannot be imported, return the original attachment
            return att
        return load_repository(att)

    # If the attachment is not a file, return it unchanged
    if not path.is_file():
        return att

    # Helper to determine if a file is binary
    def _is_binary(file_path: Path) -> bool:
        try:
            with file_path.open("rb") as f:
                chunk = f.read(8192)
            # Heuristic: if null byte or too many non-text bytes, treat as binary
            if b"\0" in chunk:
                return True
            # Count non-ASCII characters
            non_ascii = sum(1 for b in chunk if b < 32 or b > 126)
            return non_ascii > len(chunk) * 0.30
        except Exception:
            return True

    # Skip binary files
    if _is_binary(path):
        att.content = None
        return att

    # Read the file as UTF-8 text, replacing errors
    try:
        with path.open("r", encoding="utf-8", errors="replace") as f:
            att.content = f.read()
    except Exception:
        att.content = None

    return att