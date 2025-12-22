from typing import Union

class ClosestSample:
    def __init__(self, sequence_sample: str, frame_idx: int, metric_type: str, metric_value: float, reference_path: str):
        self.sequence_sample = sequence_sample
        self.frame_idx = frame_idx
        self.metric_type = metric_type
        self.metric_value = metric_value
        self.reference_path = reference_path

    def save_to_pdb(self, test_case: str, closest_dir: Union[str, bytes, os.PathLike]) -> None:
        # Implementation to save the closest sample to a PDB file in the specified directory
        pass