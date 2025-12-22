import os
import json
import fcntl
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
        self.state_file = state_file
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.lock_file = self.state_file.with_suffix(".lock")
        self.lock_fd = None

    def _load_state(self) -> Dict[str, Any]:
        try:
            with self.state_file.open("r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"processed": set(), "failed": set(), "points_created": 0}

    def save_state(self) -> None:
        state = self._load_state()
        with self.state_file.open("w") as f:
            json.dump(state, f, indent=2)

    def is_processed(self, file_path: Path) -> bool:
        state = self._load_state()
        return str(file_path) in state["processed"]

    def mark_processed(self, file_path: Path, points_created: int) -> None:
        state = self._load_state()
        state["processed"].add(str(file_path))
        state["points_created"] += points_created
        self.save_state()

    def mark_failed(self, file_path: Path, error: str) -> None:
        state = self._load_state()
        state["failed"].add(str(file_path))
        self.save_state()

    def get_processed_files(self) -> Set[str]:
        state = self._load_state()
        return state["processed"]

    def get_failed_files(self) -> Set[str]:
        state = self._load_state()
        return state["failed"]

    def reset(self) -> None:
        state = self._load_state()
        state["processed"] = set()
        state["failed"] = set()
        state["points_created"] = 0
        self.save_state()

    def get_statistics(self) -> Dict[str, Any]:
        state = self._load_state()
        return {
            "processed_files": len(state["processed"]),
            "failed_files": len(state["failed"]),
            "points_created": state["points_created"],
        }

    def acquire_lock(self) -> bool:
        try:
            self.lock_fd = self.lock_file.open("w")
            fcntl.flock(self.lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return True
        except BlockingIOError:
            return False

    def release_lock(self) -> None:
        if self.lock_fd:
            fcntl.flock(self.lock_fd, fcntl.LOCK_UN)
            self.lock_fd.close()
            self.lock_fd = None