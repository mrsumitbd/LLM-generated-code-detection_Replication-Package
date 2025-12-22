import json
import pathlib
import os
from typing import Any, Dict, Optional


class BacklogCleaner:
    """Manages a backlog of watched movies to sync when connection is restored"""

    def __init__(self, app_data_dir: pathlib.Path, backlog_file: str = "backlog.json"):
        self.app_data_dir = pathlib.Path(app_data_dir)
        self.backlog_file = backlog_file
        self.backlog_path = self.app_data_dir / self.backlog_file

        # Ensure the application data directory exists
        os.makedirs(self.app_data_dir, exist_ok=True)

        # Load existing backlog or start with an empty one
        self._load_backlog()

    def _load_backlog(self):
        """Load the backlog from the JSON file."""
        if self.backlog_path.is_file():
            try:
                with self.backlog_path.open("r", encoding="utf-8") as f:
                    self.backlog: Dict[Any, Dict[str, Any]] = json.load(f)
            except (json.JSONDecodeError, OSError):
                # If the file is corrupted or unreadable, start fresh
                self.backlog = {}
        else:
            self.backlog = {}

    def _save_backlog(self):
        """Persist the current backlog to the JSON file."""
        try:
            with self.backlog_path.open("w", encoding="utf-8") as f:
                json.dump(self.backlog, f, ensure_ascii=False, indent=2)
        except OSError as e:
            # In a real application you might want to log this
            raise RuntimeError(f"Failed to write backlog file: {e}") from e

    def add(self, simkl_id: Any, title: str, additional_data: Optional[Dict[str, Any]] = None):
        """Add a new item to the backlog."""
        if simkl_id in self.backlog:
            # If the item already exists, we don't overwrite it
            return
        self.backlog[simkl_id] = {
            "title": title,
            "additional_data": additional_data or {},
        }
        self._save_backlog()

    def get_pending(self) -> Dict[Any, Dict[str, Any]]:
        """Return a copy of all pending backlog items."""
        return dict(self.backlog)

    def update_item(self, simkl_id: Any, updates: Dict[str, Any]):
        """Update fields of an existing backlog item."""
        if simkl_id not in self.backlog:
            raise KeyError(f"Simkl ID {simkl_id} not found in backlog.")
        # Merge updates into the existing item
        self.backlog[simkl_id].update(updates)
        self._save_backlog()

    def remove(self, simkl_id: Any):
        """Remove an item from the backlog."""
        if simkl_id in self.backlog:
            del self.backlog[simkl_id]
            self._save_backlog()

    def clear(self):
        """Clear all items from the backlog."""
        self.backlog.clear()
        self._save_backlog()

    def has_pending_items(self) -> bool:
        """Return True if there are any items pending in the backlog."""
        return bool(self.backlog)