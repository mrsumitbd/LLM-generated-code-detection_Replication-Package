from typing import List, Union
import json

StrPath = Union[str, bytes]

class LocalResidInfo:
    def __init__(self, resid_list: List[int]):
        self.resid_list = resid_list

    @classmethod
    def from_json(cls, json_file: StrPath, n_residues: int):
        with open(json_file, 'r') as f:
            data = json.load(f)
        resid_ranges = data['resid_ranges']
        return cls(cls.to_explicit_resids(resid_ranges, n_residues))

    def parse_range(self, r: List[int | None]) -> tuple[int, int]:
        start = r[0] if r[0] is not None else 1
        end = r[1] if r[1] is not None else self.n_residues
        return start, end

    def to_explicit_resids(self, resid_ranges: List[List[int | None]], n_residues: int) -> List[int]:
        explicit_resids = []
        for r in resid_ranges:
            start, end = self.parse_range(r)
            for i in range(start, end + 1):
                explicit_resids.append(i)
        return explicit_resids

    def __post_init__(self) -> None:
        self.n_residues = len(self.resid_list)