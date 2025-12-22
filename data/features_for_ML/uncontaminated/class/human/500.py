import json
from bioemu_benchmarks.utils import StrPath, tqdm_joblib

class LocalResidInfo:
    alignment_resid_ranges: list[list[int | None]] | None  # ranges of residues to align upon
    metric_resid_ranges: list[list[int | None]]  # ranges of residues to compute metrics on
    n_residues: int  # maximum number of residue indices between all conformations of a single
    # test case id (or number of columns in their MSA)

    @classmethod
    def from_json(cls, json_file: StrPath, n_residues: int):
        """Parses alignment and metric residue information from JSON file"""
        with open(json_file) as json_handle:
            localresid_dict = json.load(json_handle)
        return cls(**localresid_dict, n_residues=n_residues)

    def parse_range(self, r: list[int | None]) -> tuple[int, int]:
        """
        Parses either an alignment or a metric range, in the format `[idx_i, idx_j]`, where
        `idx_x` can be `:`, representing _up to_, or _from_ in the Python slice sense, and
        returns explicit residue begin/end indices in the format `(begin_resid, end_resid)`.
        """
        assert len(r) == 2
        if r[0] is None:
            begin_resid = 1
        else:
            assert isinstance(r[0], int)  # shut up mypy
            begin_resid = r[0]

        if r[1] is None:
            end_resid = self.n_residues
        else:
            assert isinstance(r[1], int)  # shut up mypy
            end_resid = r[1]

        assert isinstance(begin_resid, int) and isinstance(end_resid, int)  # shut up mypy
        assert begin_resid <= end_resid
        return begin_resid, end_resid

    def to_explicit_resids(self, resid_ranges: list[list[int | None]]) -> list[int]:
        """Converts a list of resid ranges into an explicit residue index list"""
        explicit_resids: list[int] = []
        last_e_idx = -1
        for r in resid_ranges:
            b_idx, e_idx = self.parse_range(r)
            if e_idx > self.n_residues:
                explicit_resids.extend(list(range(b_idx, self.n_residues + 1)))
                return explicit_resids
            assert b_idx > last_e_idx  # ensure ascending order
            explicit_resids.extend(list(range(b_idx, e_idx + 1)))
            last_e_idx = e_idx
        return explicit_resids

    def __post_init__(self) -> None:
        self.alignment_resids: list[int] = []  # explicit alignment residue indices
        self.metric_resids: list[int] = []  # explicit metric residue indices

        if self.alignment_resid_ranges is not None:
            self.alignment_resids = self.to_explicit_resids(self.alignment_resid_ranges)

        self.metric_resids = self.to_explicit_resids(self.metric_resid_ranges)