import os
from pathlib import Path
from typing import List, Optional

def _list_checkpoint_files(model_id: Optional[str] = None) -> List[str]:
    """
    Core implementation of listing checkpoint files.

    Args:
        model_id: Optional model identifier to filter checkpoints

    Returns:
        List of checkpoint paths
    """
    # Default checkpoint directory (relative to this file)
    base_dir = Path(__file__).parent / "checkpoints"

    # If the directory does not exist, return an empty list
    if not base_dir.is_dir():
        return []

    # Gather all files in the checkpoint directory
    all_files = [p for p in base_dir.iterdir() if p.is_file()]

    # If a model_id is provided, filter files that contain the model_id in their name
    if model_id:
        filtered_files = [p for p in all_files if model_id in p.name]
    else:
        filtered_files = all_files

    # Return sorted list of absolute paths as strings
    return sorted([str(p.resolve()) for p in filtered_files])