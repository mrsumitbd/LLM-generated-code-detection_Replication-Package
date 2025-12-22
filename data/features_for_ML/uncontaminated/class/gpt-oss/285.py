from __future__ import annotations

import json
from dataclasses import dataclass, field, fields
from typing import Any, Dict, Optional


@dataclass(slots=True)
class AudioMetadata:
    """Complete metadata for an audio recording."""

    title: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    track_number: Optional[int] = None
    duration: Optional[float] = None
    bitrate: Optional[int] = None
    sample_rate: Optional[int] = None
    channels: Optional[int] = None
    codec: Optional[str] = None
    language: Optional[str] = None
    comment: Optional[str] = None

    def __post_init__(self) -> None:
        if self.year is not None and self.year < 0:
            raise ValueError("year must be non‑negative")
        if self.track_number is not None and self.track_number < 0:
            raise ValueError("track_number must be non‑negative")
        if self.duration is not None and self.duration < 0:
            raise ValueError("duration must be non‑negative")
        if self.bitrate is not None and self.bitrate < 0:
            raise ValueError("bitrate must be non‑negative")
        if self.sample_rate is not None and self.sample_rate < 0:
            raise ValueError("sample_rate must be non‑negative")
        if self.channels is not None and self.channels < 0:
            raise ValueError("channels must be non‑negative")

    # ------------------------------------------------------------------
    # Conversion helpers
    # ------------------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary of all non‑None attributes."""
        return {
            f.name: getattr(self, f.name)
            for f in fields(self)
            if getattr(self, f.name) is not None
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AudioMetadata":
        """Create an instance from a dictionary."""
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})

    def as_json(self) -> str:
        """Return a JSON string representation."""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> "AudioMetadata":
        """Create an instance from a JSON string."""
        return cls.from_dict(json.loads(json_str))

    # ------------------------------------------------------------------
    # Mutating helpers
    # ------------------------------------------------------------------
    def update(self, **kwargs: Any) -> None:
        """Update attributes from keyword arguments."""
        for key, value in kwargs.items():
            if key in self.__annotations__:
                setattr(self, key, value)
            else:
                raise AttributeError(f"{key!r} is not a valid attribute")

    def copy(self) -> "AudioMetadata":
        """Return a shallow copy of the instance."""
        return self.__class__(**self.to_dict())

    # ------------------------------------------------------------------
    # Special methods
    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.to_dict().items())
        return f"{self.__class__.__name__}({attrs})"

    def __hash__(self) -> int:
        return hash(tuple(getattr(self, f.name) for f in fields(self)))

    def __iter__(self):
        """Iterate over (attribute_name, value) pairs."""
        for f in fields(self):
            yield f.name, getattr(self, f.name)

    def __len__(self) -> int:
        """Number of non‑None attributes."""
        return len(self.to_dict())

    def __contains__(self, item: str) -> bool:
        """Check if an attribute exists and is not None."""
        return item in self.__annotations__ and getattr(self, item) is not None

    def __getitem__(self, key: str) -> Any:
        if key in self.__annotations__:
            return getattr(self, key)
        raise KeyError(key)

    def __setitem__(self, key: str, value: Any) -> None:
        if key in self.__annotations__:
            setattr(self, key, value)
        else:
            raise KeyError(key)

    def __delitem__(self, key: str) -> None:
        if key in self.__annotations__:
            setattr(self, key, None)
        else:
            raise KeyError(key)