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
        sequence_sample,
        frame_idx: int,
        metric_type: str,
        metric_value: float,
        reference_path
    ):
        self.sequence_sample = sequence_sample
        self.frame_idx = frame_idx
        self.metric_type = metric_type
        self.metric_value = metric_value
        self.reference_path = reference_path

    def save_to_pdb(self, test_case: str, closest_dir) -> None:
        import os
        import mdtraj as md
        
        # Load the trajectory
        if isinstance(self.sequence_sample, (list, tuple)):
            # If it's a tuple/list of (xtc, pdb) or similar
            traj = md.load(self.sequence_sample[0], top=self.sequence_sample[1])
        else:
            # If it's a single file path
            traj = md.load(self.sequence_sample)
        
        # Extract the specific frame
        frame = traj[self.frame_idx]
        
        # Create output filename
        filename = f"{test_case}_{self.metric_type}_{self.metric_value:.4f}.pdb"
        output_path = os.path.join(closest_dir, filename)
        
        # Ensure directory exists
        os.makedirs(closest_dir, exist_ok=True)
        
        # Save to PDB
        frame.save_pdb(output_path)