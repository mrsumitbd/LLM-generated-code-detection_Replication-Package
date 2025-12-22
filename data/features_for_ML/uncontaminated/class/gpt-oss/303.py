from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class UserSearchRefinement:
    """Schema for refining user search parameters."""
    name: Optional[str] = None
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    location: Optional[str] = None
    interests: Optional[List[str]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.min_age is not None and self.min_age < 0:
            raise ValueError("min_age must be non‑negative")
        if self.max_age is not None and self.max_age < 0:
            raise ValueError("max_age must be non‑negative")
        if self.min_age is not None and self.max_age is not None:
            if self.min_age > self.max_age:
                raise ValueError("min_age cannot be greater than max_age")
        if self.interests is None:
            self.interests = []

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the refinement, excluding None values."""
        result: Dict[str, Any] = {}
        if self.name is not None:
            result["name"] = self.name
        if self.min_age is not None:
            result["min_age"] = self.min_age
        if self.max_age is not None:
            result["max_age"] = self.max_age
        if self.location is not None:
            result["location"] = self.location
        if self.interests:
            result["interests"] = list(self.interests)
        return result

    def matches(self, user: Dict[str, Any]) -> bool:
        """
        Determine whether a user dictionary matches the refinement criteria.

        Expected keys in `user`:
            - name (str)
            - age (int)
            - location (str)
            - interests (list of str)
        """
        # Name check
        if self.name is not None:
            if "name" not in user or not isinstance(user["name"], str):
                return False
            if user["name"].lower() != self.name.lower():
                return False

        # Age check
        if "age" in user:
            age = user["age"]
            if not isinstance(age, int):
                return False
            if self.min_age is not None and age < self.min_age:
                return False
            if self.max_age is not None and age > self.max_age:
                return False
        else:
            # If age is required by the refinement but missing in user
            if self.min_age is not None or self.max_age is not None:
                return False

        # Location check
        if self.location is not None:
            if "location" not in user or not isinstance(user["location"], str):
                return False
            if user["location"].lower() != self.location.lower():
                return False

        # Interests check
        if self.interests:
            if "interests" not in user or not isinstance(user["interests"], list):
                return False
            user_interests = {i.lower() for i in user["interests"] if isinstance(i, str)}
            required = {i.lower() for i in self.interests}
            if not required.issubset(user_interests):
                return False

        return True

    def __repr__(self) -> str:
        parts = []
        if self.name is not None:
            parts.append(f"name={self.name!r}")
        if self.min_age is not None:
            parts.append(f"min_age={self.min_age}")
        if self.max_age is not None:
            parts.append(f"max_age={self.max_age}")
        if self.location is not None:
            parts.append(f"location={self.location!r}")
        if self.interests:
            parts.append(f"interests={self.interests!r}")
        return f"{self.__class__.__name__}({', '.join(parts)})"