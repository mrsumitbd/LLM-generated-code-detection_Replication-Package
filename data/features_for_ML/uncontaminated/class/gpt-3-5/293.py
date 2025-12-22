import json
import pathlib

class BacklogCleaner:
    """Manages a backlog of watched movies to sync when connection is restored"""

    def __init__(self, app_data_dir: pathlib.Path, backlog_file="backlog.json"):
        self.app_data_dir = app_data_dir
        self.backlog_file = backlog_file
        self.backlog = self._load_backlog()

    def _load_backlog(self):
        try:
            with open(self.app_data_dir / self.backlog_file, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_backlog(self):
        with open(self.app_data_dir / self.backlog_file, 'w') as file:
            json.dump(self.backlog, file, indent=4)

    def add(self, simkl_id, title, additional_data=None):
        self.backlog[simkl_id] = {'title': title, 'additional_data': additional_data}
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
        self.backlog = {}
        self._save_backlog()

    def has_pending_items(self) -> bool:
        return bool(self.backlog)