import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, Set

class StateManager:
    """
    Manage import state with atomic writes and crash recovery.
    
    Implements the critical STATE_FILE fixes:
    1. Handle empty dirname case
    2. Atomic writes to prevent corruption
    3. File locking for concurrent access
    """

    def __init__(self, state_file: Path):
        # Ensure the directory exists; handle empty dirname
        if not state_file.parent:
            state_file = Path(state_file.name)
        self.state_file = state_file
        self.lock_file = self.state_file.with_suffix('.lock')
        self._state: Dict[str, Any] = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        if not self.state_file.exists():
            return {"processed": {}, "failed": {}}
        try:
            with self.state_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
            # Ensure required keys
            data.setdefault("processed", {})
            data.setdefault("failed", {})
            return data
        except Exception:
            # Corrupted file: start fresh
            return {"processed": {}, "failed": {}}

    def save_state(self) -> None:
        # Write to a temporary file then rename atomically
        tmp_fd, tmp_path = tempfile.mkstemp(dir=self.state_file.parent, prefix=self.state_file.name, suffix=".tmp")
        try:
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as tmp_file:
                json.dump(self._state, tmp_file, indent=2)
                tmp_file.flush()
                os.fsync(tmp_file.fileno())
            os.replace(tmp_path, self.state_file)
        except Exception:
            # Clean up temp file on failure
            os.unlink(tmp_path)
            raise

    def is_processed(self, file_path: Path) -> bool:
        return str(file_path) in self._state["processed"]

    def mark_processed(self, file_path: Path, points_created: int) -> None:
        key = str(file_path)
        self._state["processed"][key] = points_created
        self._state["failed"].pop(key, None)

    def mark_failed(self, file_path: Path, error: str) -> None:
        key = str(file_path)
        self._state["failed"][key] = error
        self._state["processed"].pop(key, None)

    def get_processed_files(self) -> Set[str]:
        return set(self._state["processed"].keys())

    def get_failed_files(self) -> Set[str]:
        return set(self._state["failed"].keys())

    def reset(self) -> None:
        self._state = {"processed": {}, "failed": {}}
        self.save_state()

    def get_statistics(self) -> Dict[str, Any]:
        processed_count = len(self._state["processed"])
        failed_count = len(self._state["failed"])
        total_points = sum(self._state["processed"].values())
        return {
            "processed_count": processed_count,
            "failed_count": failed_count,
            "total_points": total_points,
        }

    def acquire_lock(self) -> bool:
        """
        Attempt to acquire an exclusive lock by creating a lock file.
        Returns True if lock acquired, False otherwise.
        """
        try:
            # O_CREAT | O_EXCL ensures atomic creation
            fd = os.open(self.lock_file, os.O_CREAT | os.O_EXCL | os.O_RDWR)
            os.close(fd)
            return True
        except FileExistsError:
            return False

    def release_lock(self) -> None:
        """
        Release the lock by removing the lock file.
        """
        try:
            os.unlink(self.lock_file)
        except FileNotFoundError:
            pass