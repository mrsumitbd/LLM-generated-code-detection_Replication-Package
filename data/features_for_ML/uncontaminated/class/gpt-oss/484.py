from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union


@dataclass(frozen=True)
class ToolDefinition:
    """Tool definition with metadata."""

    name: str
    description: str = ""
    version: str = "1.0"
    author: str = ""
    license: str = ""
    tags: Tuple[str, ...] = field(default_factory=tuple)
    parameters: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("Tool name must not be empty.")
        if not re.match(r"^\d+\.\d+(\.\d+)?$", self.version):
            raise ValueError(f"Invalid version format: {self.version!r}. Expected 'X.Y' or 'X.Y.Z'.")
        if not isinstance(self.tags, (list, tuple)):
            raise TypeError("tags must be a list or tuple of strings.")
        if not all(isinstance(tag, str) for tag in self.tags):
            raise TypeError("All tags must be strings.")
        if not isinstance(self.parameters, dict):
            raise TypeError("parameters must be a dictionary.")

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name={self.name!r}, "
            f"description={self.description!r}, "
            f"version={self.version!r}, "
            f"author={self.author!r}, "
            f"license={self.license!r}, "
            f"tags={self.tags!r}, "
            f"parameters={self.parameters!r})"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the tool definition."""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "author": self.author,
            "license": self.license,
            "tags": list(self.tags),
            "parameters": self.parameters,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ToolDefinition":
        """Create a ToolDefinition instance from a dictionary."""
        return cls(
            name=data["name"],
            description=data.get("description", ""),
            version=data.get("version", "1.0"),
            author=data.get("author", ""),
            license=data.get("license", ""),
            tags=tuple(data.get("tags", [])),
            parameters=data.get("parameters", {}),
        )

    def to_json(self, *, indent: Optional[int] = None) -> str:
        """Serialize the tool definition to a JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_json(cls, json_str: str) -> "ToolDefinition":
        """Deserialize a JSON string into a ToolDefinition instance."""
        data = json.loads(json_str)
        if not isinstance(data, dict):
            raise ValueError("JSON must represent an object.")
        return cls.from_dict(data)

    def update(self, **kwargs: Any) -> "ToolDefinition":
        """Return a new ToolDefinition with updated fields."""
        data = self.to_dict()
        data.update(kwargs)
        return self.__class__.from_dict(data)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ToolDefinition):
            return NotImplemented
        return self.to_dict() == other.to_dict()

    def __hash__(self) -> int:
        return hash((
            self.name,
            self.description,
            self.version,
            self.author,
            self.license,
            self.tags,
            frozenset(self.parameters.items()),
        ))