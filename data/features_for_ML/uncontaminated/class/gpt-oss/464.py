from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class SaveDocumentOutput:
    """
    Output of the save_docling_document tool.

    Attributes
    ----------
    success : bool
        Indicates whether the document was saved successfully.
    file_path : Optional[Path]
        Path to the saved document. ``None`` if the operation failed.
    message : Optional[str]
        Human‑readable message describing the outcome.
    metadata : Dict[str, Any]
        Optional dictionary containing additional information
        (e.g. file size, checksum, etc.).
    """

    success: bool
    file_path: Optional[Path] = None
    message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.success and self.file_path is None:
            raise ValueError("file_path must be provided when success is True")
        if not self.success and self.file_path is not None:
            # If the operation failed we ignore the path but keep it for debugging
            pass

    def to_dict(self) -> Dict[str, Any]:
        """Return a serialisable dictionary representation."""
        return {
            "success": self.success,
            "file_path": str(self.file_path) if self.file_path else None,
            "message": self.message,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SaveDocumentOutput":
        """Create an instance from a dictionary."""
        return cls(
            success=bool(data.get("success", False)),
            file_path=Path(data["file_path"]) if data.get("file_path") else None,
            message=data.get("message"),
            metadata=dict(data.get("metadata", {})),
        )

    def to_json(self) -> str:
        """Return a JSON string representation."""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> "SaveDocumentOutput":
        """Create an instance from a JSON string."""
        return cls.from_dict(json.loads(json_str))

    def __str__(self) -> str:
        if self.success:
            return f"Saved to {self.file_path}"
        return f"Failed: {self.message or 'Unknown error'}"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"success={self.success!r}, "
            f"file_path={self.file_path!r}, "
            f"message={self.message!r}, "
            f"metadata={self.metadata!r})"
        )