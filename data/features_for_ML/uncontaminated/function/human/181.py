from pathlib import Path
from typing import Any, Dict, List, Optional, TypeVar, Type
from plexe.config import config

def _list_checkpoint_files(model_id: Optional[str] = None) -> List[str]:
    """
    Core implementation of listing checkpoint files.

    Args:
        model_id: Optional model identifier to filter checkpoints

    Returns:
        List of checkpoint paths
    """
    checkpoint_dir = Path(config.file_storage.cache_dir) / config.file_storage.checkpoint_dir
    if not checkpoint_dir.exists():
        return []

    checkpoints = list(checkpoint_dir.glob("*.checkpoint.tar.gz"))

    if model_id:
        checkpoints = [cp for cp in checkpoints if model_id in cp.stem]

    return [str(cp) for cp in checkpoints]