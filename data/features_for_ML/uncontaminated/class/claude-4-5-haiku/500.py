from dataclasses import dataclass, field
from pathlib import Path
from typing import Union
import json

StrPath = Union[str, Path]

@dataclass
class LocalResidInfo:
    resid_ranges: list[list[int | None]] = field(default_factory=list)
    explicit_resids: list[int] = field(default_factory=list)
    n_residues: int = 0

    @classmethod
    def from_json(cls, json_file: StrPath, n_residues: int):
        json_file = Path(json_file)
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        resid_ranges = data.get('resid_ranges', [])
        explicit_resids = data.get('explicit_resids', [])
        
        instance = cls(
            resid_ranges=resid_ranges,
            explicit_resids=explicit_resids,
            n_residues=n_residues
        )
        instance.__post_init__()
        return instance

    def parse_range(self, r: list[int | None]) -> tuple[int, int]:
        start = r[0] if r[0] is not None else 0
        end = r[1] if r[1] is not None else self.n_residues - 1
        
        if start < 0:
            start = self.n_residues + start
        if end < 0:
            end = self.n_residues + end
        
        start = max(0, min(start, self.n_residues - 1))
        end = max(0, min(end, self.n_residues - 1))
        
        return (start, end)

    def to_explicit_resids(self, resid_ranges: list[list[int | None]]) -> list[int]:
        resids = []
        for r in resid_ranges:
            start, end = self.parse_range(r)
            resids.extend(range(start, end + 1))
        return sorted(list(set(resids)))

    def __post_init__(self) -> None:
        if self.resid_ranges:
            self.explicit_resids = self.to_explicit_resids(self.resid_ranges)
        elif not self.explicit_resids:
            self.explicit_resids = list(range(self.n_residues))