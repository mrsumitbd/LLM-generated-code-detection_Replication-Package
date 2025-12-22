import json
import pathlib

class BacklogCleaner:
    """Manages a backlog of watched movies to sync when connection is restored"""

    def __init__(self, app_data_dir: pathlib.Path, backlog_file="backlog.json"):
        self.backlog_file = app_data_dir / backlog_file
        self.backlog = self._load_backlog()

    def _load_backlog(self):
        try:
            with self.backlog_file.open("r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_backlog(self):
        with self.backlog_file.open("w") as f:
            json.dump(self.backlog, f, indent=2)

    def add(self, simkl_id, title, additional_data=None):
        self.backlog[simkl_id] = {"title": title, "additional_data": additional_data}
        self._save_backlog()

    def get_pending(self) -> dict:
        return self.backlog

    def update_item(self, simkl_id, updates: dict):
        if simkl_id in self.backlog:
            self.backlog[simkl_id].update(updates)
            self._save_backlog()

    def remove(self, simkl_id):
        if simkl_id in self.backlog:
            del self.backlog[simkl_id]
            self._save_backlog()

    def clear(self):
        self.backlog.clear()
        self._save_backlog()

    def has_pending_items(self) -> bool:
        return bool(self.backlog)