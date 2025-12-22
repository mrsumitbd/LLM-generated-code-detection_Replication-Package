import json
from typing import Dict, Any

class UserDataManager:

    def __init__(self, file_path: str = "./UserData.json"):
        self.file_path = file_path
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def _save(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file, indent=4)

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def set(self, key: str, value: Any):
        self.data[key] = value
        self._save()