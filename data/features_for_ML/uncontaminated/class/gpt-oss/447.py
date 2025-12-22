from __future__ import annotations

import shutil
from pathlib import Path
from typing import Union, Optional

# Type alias for a string or pathlib.Path
StrPath = Union[str, Path]


class ClosestSample:
    """
    Keeps information about the closest sample to a given reference.

    Args:
        sequence_sample: XTC/PDB paths to sample file
        frame_idx: Frame index where closest sample in the XTC file is located
        metric_type: The type of metric that was computed
        metric_value: The associated numerical value of that metric against the reference
        reference_path: Path to the reference PDB file
    """

    def __init__(
        self,
        sequence_sample: StrPath,
        frame_idx: Optional[int],
        metric_type: str,
        metric_value: float,
        reference_path: StrPath,
    ) -> None:
        self.sequence_sample = Path(sequence_sample)
        self.frame_idx = frame_idx
        self.metric_type = metric_type
        self.metric_value = metric_value
        self.reference_path = Path(reference_path)

    def _ensure_dir(self, dir_path: Path) -> None:
        """Create directory if it does not exist."""
        dir_path.mkdir(parents=True, exist_ok=True)

    def _copy_pdb(self, dest: Path) -> None:
        """Copy a PDB file to the destination."""
        shutil.copyfile(self.sequence_sample, dest)

    def _write_xtc_frame(self, dest: Path) -> None:
        """
        Write a single frame from an XTC trajectory to a PDB file.

        The topology file is expected to be in the same directory as the XTC
        and have the same stem with a .pdb, .gro or .prmtop extension.
        """
        try:
            import MDAnalysis as mda
        except ImportError as exc:
            raise RuntimeError(
                "MDAnalysis is required to read XTC files but is not installed."
            ) from exc

        # Find a suitable topology file
        xtc_dir = self.sequence_sample.parent
        stem = self.sequence_sample.stem
        topo_candidates = [
            xtc_dir / f"{stem}.pdb",
            xtc_dir / f"{stem}.gro",
            xtc_dir / f"{stem}.prmtop",
        ]
        topo_path = next((p for p in topo_candidates if p.is_file()), None)
        if topo_path is None:
            raise FileNotFoundError(
                f"No topology file found for {self.sequence_sample!s}. "
                f"Expected one of: {', '.join(str(p) for p in topo_candidates)}"
            )

        u = mda.Universe(str(topo_path), str(self.sequence_sample))
        if self.frame_idx is None:
            frame = 0
        else:
            frame = self.frame_idx
        if frame < 0 or frame >= len(u.trajectory):
            raise IndexError(
                f"frame_idx {frame} is out of bounds for trajectory "
                f"with {len(u.trajectory)} frames."
            )
        u.trajectory[frame]
        u.atoms.write(str(dest))

    def save_to_pdb(self, test_case: str, closest_dir: StrPath) -> None:
        """
        Save the closest sample to a PDB file in the specified directory.

        The output file is named using the test case, metric type and value:
        ``{test_case}_{metric_type}_{metric_value:.4f}.pdb``.
        """
        dest_dir = Path(closest_dir)
        self._ensure_dir(dest_dir)

        # Format metric value to avoid too many decimals
        metric_str = f"{self.metric_value:.4f}".replace(".", "_")
        dest_name = f"{test_case}_{self.metric_type}_{metric_str}.pdb"
        dest_path = dest_dir / dest_name

        if self.sequence_sample.suffix.lower() == ".pdb":
            self._copy_pdb(dest_path)
        elif self.sequence_sample.suffix.lower() == ".xtc":
            self._write_xtc_frame(dest_path)
        else:
            raise ValueError(
                f"Unsupported file type {self.sequence_sample.suffix!r}. "
                "Only .pdb and .xtc are supported."
            )