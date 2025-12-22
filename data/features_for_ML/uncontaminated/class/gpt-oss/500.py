from __future__ import annotations

import json
import pathlib
from dataclasses import dataclass, field
from typing import Iterable, List, Sequence, Tuple, Union

StrPath = Union[str, pathlib.Path]


@dataclass
class LocalResidInfo:
    """
    Holds residue ranges and provides utilities to convert them to explicit residue
    indices. Ranges are specified as [start, end] where either element may be
    ``None`` to indicate the beginning or end of the sequence.
    """
    resid_ranges: List[List[Union[int, None]]]
    n_residues: int
    explicit_resids: List[int] = field(init=False)

    @classmethod
    def from_json(cls, json_file: StrPath, n_residues: int) -> "LocalResidInfo":
        """
        Load residue ranges from a JSON file and create a ``LocalResidInfo`` instance.

        The JSON file must contain a list of two‑element lists, each representing a
        range. ``None`` may be used to indicate the start or end of the sequence.
        """
        path = pathlib.Path(json_file)
        data = json.loads(path.read_text())

        if not isinstance(data, Sequence):
            raise ValueError("JSON must contain a sequence of ranges")

        ranges: List[List[Union[int, None]]] = []
        for r in data:
            if not isinstance(r, Sequence) or len(r) != 2:
                raise ValueError(f"Invalid range format: {r!r}")
            start, end = r
            if start is not None and not isinstance(start, int):
                raise ValueError(f"Start must be int or None, got {start!r}")
            if end is not None and not isinstance(end, int):
                raise ValueError(f"End must be int or None, got {end!r}")
            ranges.append([start, end])

        return cls(ranges, n_residues)

    def parse_range(self, r: Sequence[Union[int, None]]) -> Tuple[int, int]:
        """
        Convert a range specification to a concrete (start, end) tuple.

        ``None`` is interpreted as the beginning (1) or the end (``n_residues``)
        of the sequence.
        """
        if len(r) != 2:
            raise ValueError(f"Range must have two elements, got {r!r}")

        start, end = r
        if start is None:
            start = 1
        if end is None:
            end = self.n_residues

        if not (1 <= start <= self.n_residues):
            raise ValueError(f"Start {start} out of bounds (1..{self.n_residues})")
        if not (1 <= end <= self.n_residues):
            raise ValueError(f"End {end} out of bounds (1..{self.n_residues})")
        if start > end:
            raise ValueError(f"Start {start} greater than end {end}")

        return start, end

    def to_explicit_resids(self, resid_ranges: List[List[Union[int, None]]]) -> List[int]:
        """
        Expand a list of range specifications into a flat list of residue indices.
        """
        resids: List[int] = []
        for r in resid_ranges:
            start, end = self.parse_range(r)
            resids.extend(range(start, end + 1))
        return resids

    def __post_init__(self) -> None:
        """
        Compute the explicit residue list after initialization.
        """
        self.explicit_resids = self.to_explicit_resids(self.resid_ranges)