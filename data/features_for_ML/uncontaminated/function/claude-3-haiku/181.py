import os
from typing import List, Optional

def _list_checkpoint_files(model_id: Optional[str] = None) -> List[str]:
    """
    Core implementation of listing checkpoint files.

    Args:
        model_id: Optional model identifier to filter checkpoints

    Returns:
        List of checkpoint paths
    """
    checkpoint_dir = os.path.join("models", "checkpoints")
    checkpoint_files = [f for f in os.listdir(checkpoint_dir) if f.endswith(".ckpt")]

    if model_id:
        checkpoint_files = [f for f in checkpoint_files if model_id in f]

    return [os.path.join(checkpoint_dir, f) for f in checkpoint_files]