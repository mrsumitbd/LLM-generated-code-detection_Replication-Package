import os
import tempfile
import json
from typing import Optional, Dict, List

class StorageManager:
    def __init__(self):
        self._executable_path = self.get_executable_path()
        self._base_path = self.get_base_path()
        self._temp_files = []

    def get_executable_path(self) -> str:
        import sys
        return sys.executable

    def get_base_path(self) -> str:
        if self.is_frozen():
            return os.path.dirname(self._executable_path)
        else:
            return os.path.dirname(os.path.abspath(__file__))

    def is_frozen(self) -> bool:
        return hasattr(sys, 'frozen') and sys.frozen

    def is_running_from_source(self) -> bool:
        return not self.is_frozen()

    def _verify_and_merge_config(self, original: Optional[Dict], new_data: Optional[Dict]) -> Dict:
        if original is None:
            original = {}
        if new_data is None:
            new_data = {}
        return {**original, **new_data}

    def _generate_key(self, path_root: str = "base", sub_path: str = "save") -> None:
        pass

    def _load_key(self, path_root: str = "base", sub_path: str = "save") -> Optional[bytes]:
        pass

    def get_path(self, path_root: str = "base", relative_path: Optional[str] = None) -> Optional[str]:
        if path_root == "base":
            return os.path.join(self._base_path, relative_path) if relative_path else self._base_path
        else:
            return None

    def get_existing_path(self, path_root: str = "base", relative_path: Optional[str] = None) -> Optional[str]:
        path = self.get_path(path_root, relative_path)
        return path if os.path.exists(path) else None

    def save_config(self, path_root: str = "base", sub_path: str = "save", new: Optional[Dict] = None, original: Optional[Dict] = None) -> None:
        config = self._verify_and_merge_config(original, new)
        path = self.get_path(path_root, sub_path)
        with open(path, 'w') as f:
            json.dump(config, f)

    def load_config(self, path_root: str = "base", sub_path: str = "save", original: Optional[Dict] = None) -> Dict:
        path = self.get_existing_path(path_root, sub_path)
        if path:
            with open(path, 'r') as f:
                return self._verify_and_merge_config(original, json.load(f))
        else:
            return self._verify_and_merge_config(original, None)

    def delete_file(self, path_root: str = "base", relative_path: Optional[str] = None) -> bool:
        path = self.get_existing_path(path_root, relative_path)
        if path:
            os.remove(path)
            return True
        else:
            return False

    def create_temp_txt(self, content: str = "") -> str:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write(content)
            temp_path = temp_file.name
            self._temp_files.append(temp_path)
        return temp_path

    def get_temp_files(self) -> List[str]:
        return self._temp_files

    def get_last_temp_file(self) -> Optional[str]:
        if self._temp_files:
            return self._temp_files[-1]
        else:
            return None

    def get_latest_version(self) -> Optional[str]:
        pass