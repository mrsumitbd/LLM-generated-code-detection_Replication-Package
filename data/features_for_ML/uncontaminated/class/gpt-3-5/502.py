from pathlib import Path
from typing import Dict, Any, Set

class StateManager:
    """
    Manage import state with atomic writes and crash recovery.
    
    Implements the critical STATE_FILE fixes:
    1. Handle empty dirname case
    2. Atomic writes to prevent corruption
    3. File locking for concurrent access
    """

    def __init__(self, state_file: Path):
        pass

    def _load_state(self) -> Dict[str, Any]:
        pass

    def save_state(self) -> None:
        pass

    def is_processed(self, file_path: Path) -> bool:
        pass

    def mark_processed(self, file_path: Path, points_created: int) -> None:
        pass

    def mark_failed(self, file_path: Path, error: str) -> None:
        pass

    def get_processed_files(self) -> Set[str]:
        pass

    def get_failed_files(self) -> Set[str]:
        pass

    def reset(self) -> None:
        pass

    def get_statistics(self) -> Dict[str, Any]:
        pass

    def acquire_lock(self) -> bool:
        pass

    def release_lock(self) -> None:
        pass