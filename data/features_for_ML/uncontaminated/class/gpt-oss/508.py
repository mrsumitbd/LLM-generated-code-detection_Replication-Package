from __future__ import annotations
from dataclasses import dataclass
from typing import List


@dataclass
class Completion:
    """Simple representation of a well completion."""
    I: int
    J: int
    K: int
    stat: int  # 1 for active, 0 for inactive

    @property
    def is_active(self) -> bool:
        return self.stat == 1


class Well:
    """Represents a well.

    A well has a name, type (producer or injector), and a list of completions.

    Attributes:
        name (str): Name of the well.
        type (str): Type of well ("PRD" or "INJ").
        completions (list[Completion]): List of Completion objects associated with the well.
        num_active_completions (int): Number of active (open) completions.
    """

    _TYPE_MAP = {1: "PRD", 2: "INJ"}

    def __init__(self, name: str, type_id: int) -> None:
        self.name: str = name
        self._set_type(type_id)
        self.completions: List[Completion] = []
        self.num_active_completions: int = 0

    def add_completion(self, I: int, J: int, K: int, stat: int) -> None:
        """Add a completion to the well."""
        comp = Completion(I, J, K, stat)
        self.completions.append(comp)
        if comp.is_active:
            self.num_active_completions += 1

    def set_status(self) -> None:
        """Recalculate the number of active completions."""
        self.num_active_completions = sum(1 for c in self.completions if c.is_active)

    def _set_type(self, type_id: int) -> None:
        """Set the well type based on an integer identifier."""
        try:
            self.type = self._TYPE_MAP[type_id]
        except KeyError as exc:
            raise ValueError(f"Unknown type_id {type_id}") from exc