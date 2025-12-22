from typing import StrPath

class LocalResidInfo:
    def __init__(self, resid_ranges: list[list[int | None]]):
        self.resid_ranges = resid_ranges
        self.__post_init__()

    @classmethod
    def from_json(cls, json_file: StrPath, n_residues: int):
        import json
        with open(json_file, 'r') as f:
            data = json.load(f)
        resid_ranges = data['resid_ranges']
        return cls(resid_ranges)

    def parse_range(self, r: list[int | None]) -> tuple[int, int]:
        start = r[0] if r[0] is not None else 1
        end = r[1] if r[1] is not None else n_residues
        return start, end

    def to_explicit_resids(self, resid_ranges: list[list[int | None]]) -> list[int]:
        explicit_resids = []
        for r in resid_ranges:
            start, end = self.parse_range(r)
            explicit_resids.extend(range(start, end + 1))
        return sorted(set(explicit_resids))

    def __post_init__(self) -> None:
        self.explicit_resids = self.to_explicit_resids(self.resid_ranges)