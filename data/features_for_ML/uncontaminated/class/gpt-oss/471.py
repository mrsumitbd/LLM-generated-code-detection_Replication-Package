from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Tuple, Union


Chunk = Tuple[Any, Any]  # (id, data)
ModifiedChunk = Tuple[Any, Any, Any]  # (id, new_data, old_data)


@dataclass(frozen=True)
class ChunkDiff:
    """
    Represents differences between new and existing chunks for smart updates.
    """
    added: List[Chunk] = field(default_factory=list)
    removed: List[Chunk] = field(default_factory=list)
    modified: List[ModifiedChunk] = field(default_factory=list)

    @staticmethod
    def diff(
        new_chunks: Iterable[Chunk],
        existing_chunks: Iterable[Chunk],
    ) -> "ChunkDiff":
        """
        Compute the difference between two collections of chunks.
        Each chunk is expected to be a tuple (id, data).
        """
        new_dict: Dict[Any, Any] = {cid: data for cid, data in new_chunks}
        existing_dict: Dict[Any, Any] = {cid: data for cid, data in existing_chunks}

        added: List[Chunk] = [
            (cid, data) for cid, data in new_dict.items() if cid not in existing_dict
        ]
        removed: List[Chunk] = [
            (cid, data) for cid, data in existing_dict.items() if cid not in new_dict
        ]
        modified: List[ModifiedChunk] = [
            (cid, new_dict[cid], existing_dict[cid])
            for cid in new_dict
            if cid in existing_dict and new_dict[cid] != existing_dict[cid]
        ]

        return ChunkDiff(added=added, removed=removed, modified=modified)

    def apply(self, existing_chunks: Iterable[Chunk]) -> List[Chunk]:
        """
        Apply the diff to a collection of existing chunks and return the updated list.
        """
        existing_dict: Dict[Any, Any] = {cid: data for cid, data in existing_chunks}

        # Remove chunks
        for cid, _ in self.removed:
            existing_dict.pop(cid, None)

        # Modify chunks
        for cid, new_data, _ in self.modified:
            if cid in existing_dict:
                existing_dict[cid] = new_data

        # Add new chunks
        for cid, data in self.added:
            existing_dict[cid] = data

        # Return sorted list by id for consistency
        return sorted(existing_dict.items(), key=lambda x: x[0])

    def is_empty(self) -> bool:
        """Return True if there are no differences."""
        return not (self.added or self.removed or self.modified)

    def merge(self, other: "ChunkDiff") -> "ChunkDiff":
        """
        Merge another ChunkDiff into this one.
        The resulting diff contains the union of added, removed, and modified entries.
        """
        added_set = {(cid, data) for cid, data in self.added}
        added_set.update((cid, data) for cid, data in other.added)

        removed_set = {(cid, data) for cid, data in self.removed}
        removed_set.update((cid, data) for cid, data in other.removed)

        modified_set = {(cid, new, old) for cid, new, old in self.modified}
        modified_set.update((cid, new, old) for cid, new, old in other.modified)

        return ChunkDiff(
            added=list(added_set),
            removed=list(removed_set),
            modified=list(modified_set),
        )

    def to_dict(self) -> Dict[str, List[Any]]:
        """Serialize the diff to a dictionary."""
        return {
            "added": self.added,
            "removed": self.removed,
            "modified": self.modified,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChunkDiff":
        """Deserialize a diff from a dictionary."""
        return cls(
            added=data.get("added", []),
            removed=data.get("removed", []),
            modified=data.get("modified", []),
        )

    def to_json(self) -> str:
        """Serialize the diff to a JSON string."""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> "ChunkDiff":
        """Deserialize a diff from a JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)

    def __repr__(self) -> str:
        return (
            f"ChunkDiff(added={self.added!r}, "
            f"removed={self.removed!r}, modified={self.modified!r})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ChunkDiff):
            return NotImplemented
        return (
            set(self.added) == set(other.added)
            and set(self.removed) == set(other.removed)
            and set(self.modified) == set(other.modified)
        )

    def __hash__(self) -> int:
        return hash(
            (
                frozenset(self.added),
                frozenset(self.removed),
                frozenset(self.modified),
            )
        )