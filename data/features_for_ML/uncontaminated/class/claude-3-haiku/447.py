from pathlib import Path
from typing import StrPath

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

    def __init__(self, sequence_sample: StrPath, frame_idx: int, metric_type: str, metric_value: float, reference_path: StrPath):
        self.sequence_sample = sequence_sample
        self.frame_idx = frame_idx
        self.metric_type = metric_type
        self.metric_value = metric_value
        self.reference_path = reference_path

    def save_to_pdb(self, test_case: str, closest_dir: StrPath) -> None:
        # Create the output directory if it doesn't exist
        closest_dir_path = Path(closest_dir)
        closest_dir_path.mkdir(parents=True, exist_ok=True)

        # Construct the output file path
        output_file = closest_dir_path / f"{test_case}_{self.frame_idx}.pdb"

        # Save the closest sample to the output file
        if self.sequence_sample.endswith(".xtc"):
            # Code to extract the frame from the XTC file and save it to the output file
            pass
        else:
            # Copy the PDB file to the output directory
            output_file.write_bytes(Path(self.sequence_sample).read_bytes())