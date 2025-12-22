import json
import os
import tempfile
from pathlib import Path
from typing import Dict, Any, Set
from datetime import datetime
import fcntl
import sys


class StateManager:
    """
    Manage import state with atomic writes and crash recovery.
    
    Implements the critical STATE_FILE fixes:
    1. Handle empty dirname case
    2. Atomic writes to prevent corruption
    3. File locking for concurrent access
    """

    def __init__(self, state_file: Path):
        self.state_file = Path(state_file)
        self.lock_file = self.state_file.with_suffix('.lock')
        self.lock_fd = None
        self.state = {
            'processed_files': {},
            'failed_files': {},
            'statistics': {
                'total_processed': 0,
                'total_points_created': 0,
                'total_failed': 0,
                'last_updated': None
            }
        }
        self._ensure_state_dir()
        self.state = self._load_state()

    def _ensure_state_dir(self) -> None:
        """Ensure state file directory exists, handling empty dirname case."""
        dirname = self.state_file.parent
        if dirname and dirname != Path('.'):
            dirname.mkdir(parents=True, exist_ok=True)

    def _load_state(self) -> Dict[str, Any]:
        """Load state from file, with crash recovery."""
        if not self.state_file.exists():
            return {
                'processed_files': {},
                'failed_files': {},
                'statistics': {
                    'total_processed': 0,
                    'total_points_created': 0,
                    'total_failed': 0,
                    'last_updated': None
                }
            }
        
        try:
            with open(self.state_file, 'r') as f:
                data = json.load(f)
                return data
        except (json.JSONDecodeError, IOError):
            # Corrupted file, return fresh state
            return {
                'processed_files': {},
                'failed_files': {},
                'statistics': {
                    'total_processed': 0,
                    'total_points_created': 0,
                    'total_failed': 0,
                    'last_updated': None
                }
            }

    def save_state(self) -> None:
        """Save state atomically to prevent corruption."""
        self._ensure_state_dir()
        
        # Update timestamp
        self.state['statistics']['last_updated'] = datetime.now().isoformat()
        
        # Write to temporary file first
        temp_fd, temp_path = tempfile.mkstemp(
            dir=self.state_file.parent if self.state_file.parent != Path('.') else None,
            prefix='.tmp_state_',
            suffix='.json'
        )
        
        try:
            with os.fdopen(temp_fd, 'w') as f:
                json.dump(self.state, f, indent=2)
            
            # Atomic rename
            if sys.platform == 'win32':
                # Windows requires removing target first
                if self.state_file.exists():
                    self.state_file.unlink()
            
            Path(temp_path).replace(self.state_file)
        except Exception:
            # Clean up temp file on error
            try:
                Path(temp_path).unlink()
            except Exception:
                pass
            raise

    def is_processed(self, file_path: Path) -> bool:
        """Check if file has been processed."""
        return str(file_path) in self.state['processed_files']

    def mark_processed(self, file_path: Path, points_created: int) -> None:
        """Mark file as processed."""
        file_key = str(file_path)
        self.state['processed_files'][file_key] = {
            'timestamp': datetime.now().isoformat(),
            'points_created': points_created
        }
        
        # Remove from failed if it was there
        self.state['failed_files'].pop(file_key, None)
        
        # Update statistics
        self.state['statistics']['total_processed'] += 1
        self.state['statistics']['total_points_created'] += points_created
        
        self.save_state()

    def mark_failed(self, file_path: Path, error: str) -> None:
        """Mark file as failed."""
        file_key = str(file_path)
        self.state['failed_files'][file_key] = {
            'timestamp': datetime.now().isoformat(),
            'error': error
        }
        
        # Remove from processed if it was there
        self.state['processed_files'].pop(file_key, None)
        
        # Update statistics
        self.state['statistics']['total_failed'] += 1
        
        self.save_state()

    def get_processed_files(self) -> Set[str]:
        """Get set of processed file paths."""
        return set(self.state['processed_files'].keys())

    def get_failed_files(self) -> Set[str]:
        """Get set of failed file paths."""
        return set(self.state['failed_files'].keys())

    def reset(self) -> None:
        """Reset all state."""
        self.state = {
            'processed_files': {},
            'failed_files': {},
            'statistics': {
                'total_processed': 0,
                'total_points_created': 0,
                'total_failed': 0,
                'last_updated': None
            }
        }
        self.save_state()

    def get_statistics(self) -> Dict[str, Any]:
        """Get current statistics."""
        return self.state['statistics'].copy()

    def acquire_lock(self) -> bool:
        """Acquire file lock for concurrent access control."""
        try:
            self._ensure_state_dir()
            self.lock_fd = open(self.lock_file, 'w')
            fcntl.flock(self.lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return True
        except (IOError, OSError):
            if self.lock_fd:
                self.lock_fd.close()
                self.lock_fd = None
            return False

    def release_lock(self) -> None:
        """Release file lock."""
        if self.lock_fd:
            try:
                fcntl.flock(self.lock_fd, fcntl.LOCK_UN)
                self.lock_fd.close()
            except (IOError, OSError):
                pass
            finally:
                self.lock_fd = None