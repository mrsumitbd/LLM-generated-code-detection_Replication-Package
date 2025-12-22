import os
from bioemu_benchmarks.samples import IndexedSamples, SequenceSample
from bioemu_benchmarks.utils import StrPath, tqdm_joblib
import mdtraj

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

    sequence_sample: SequenceSample
    frame_idx: int
    metric_type: MetricType
    metric_value: float
    reference_path: StrPath

    def save_to_pdb(self, test_case: str, closest_dir: StrPath) -> None:
        dirpath = os.path.join(closest_dir, test_case, self.metric_type.value)

        os.makedirs(dirpath, exist_ok=True)
        filename = os.path.splitext(os.path.basename(self.reference_path))[0]
        outfile = os.path.join(dirpath, f"{filename}.pdb")

        traj = mdtraj.load(
            self.sequence_sample.trajectory_file, top=self.sequence_sample.topology_file
        )
        traj[self.frame_idx].save_pdb(outfile)