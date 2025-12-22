import pathlib
import json
from typing import Optional


class BacklogCleaner:
    """Manages a backlog of watched movies to sync when connection is restored"""

    def __init__(self, app_data_dir: pathlib.Path, backlog_file="backlog.json"):
        self.app_data_dir = pathlib.Path(app_data_dir)
        self.backlog_file = self.app_data_dir / backlog_file
        self.backlog = {}
        self._load_backlog()

    def _load_backlog(self):
        if self.backlog_file.exists():
            try:
                with open(self.backlog_file, 'r') as f:
                    self.backlog = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.backlog = {}
        else:
            self.backlog = {}

    def _save_backlog(self):
        self.app_data_dir.mkdir(parents=True, exist_ok=True)
        with open(self.backlog_file, 'w') as f:
            json.dump(self.backlog, f, indent=2)

    def add(self, simkl_id, title, additional_data=None):
        entry = {
            "title": title,
            "simkl_id": simkl_id
        }
        if additional_data:
            entry.update(additional_data)
        self.backlog[str(simkl_id)] = entry
        self._save_backlog()

    def get_pending(self) -> dict:
        return dict(self.backlog)

    def update_item(self, simkl_id, updates: dict):
        simkl_id_str = str(simkl_id)
        if simkl_id_str in self.backlog:
            self.backlog[simkl_id_str].update(updates)
            self._save_backlog()

    def remove(self, simkl_id):
        simkl_id_str = str(simkl_id)
        if simkl_id_str in self.backlog:
            del self.backlog[simkl_id_str]
            self._save_backlog()

    def clear(self):
        self.backlog = {}
        self._save_backlog()

    def has_pending_items(self) -> bool:
        return len(self.backlog) > 0