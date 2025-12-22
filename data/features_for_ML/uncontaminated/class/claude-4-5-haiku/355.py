import os
import sys
import json
import tempfile
from pathlib import Path
from typing import Optional, Dict, List
from cryptography.fernet import Fernet


class StorageManager:

    def __init__(self):
        self._temp_files: List[str] = []
        self._encryption_key: Optional[bytes] = None

    def get_executable_path(self) -> str:
        if self.is_frozen():
            return sys.executable
        return os.path.abspath(sys.argv[0])

    def get_base_path(self) -> str:
        if self.is_frozen():
            return os.path.dirname(sys.executable)
        return os.path.dirname(os.path.abspath(sys.argv[0]))

    def is_frozen(self) -> bool:
        return getattr(sys, 'frozen', False) and hasattr(sys, 'frozen')

    def is_running_from_source(self) -> bool:
        return not self.is_frozen()

    def _verify_and_merge_config(self, original: Optional[Dict], new_data: Optional[Dict]) -> Dict:
        if original is None:
            original = {}
        if new_data is None:
            new_data = {}
        
        merged = original.copy()
        merged.update(new_data)
        return merged

    def _generate_key(self, path_root: str = "base", sub_path: str = "save") -> None:
        key_path = Path(self.get_path(path_root, sub_path))
        key_path.parent.mkdir(parents=True, exist_ok=True)
        
        key_file = key_path.parent / ".encryption_key"
        if not key_file.exists():
            key = Fernet.generate_key()
            key_file.write_bytes(key)
            self._encryption_key = key
        else:
            self._encryption_key = key_file.read_bytes()

    def _load_key(self, path_root: str = "base", sub_path: str = "save") -> Optional[bytes]:
        key_path = Path(self.get_path(path_root, sub_path))
        key_file = key_path.parent / ".encryption_key"
        
        if key_file.exists():
            return key_file.read_bytes()
        return None

    def get_path(self, path_root: str = "base", relative_path: Optional[str] = None) -> Optional[str]:
        if path_root == "base":
            base = self.get_base_path()
        else:
            base = path_root
        
        if relative_path is None:
            return base
        
        full_path = os.path.join(base, relative_path)
        return full_path

    def get_existing_path(self, path_root: str = "base", relative_path: Optional[str] = None) -> Optional[str]:
        path = self.get_path(path_root, relative_path)
        if path and os.path.exists(path):
            return path
        return None

    def save_config(self, path_root: str = "base", sub_path: str = "save", new: Optional[Dict] = None, original: Optional[Dict] = None) -> None:
        merged_config = self._verify_and_merge_config(original, new)
        
        config_path = Path(self.get_path(path_root, sub_path))
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        config_file = config_path.parent / "config.json"
        config_file.write_text(json.dumps(merged_config, indent=2))

    def load_config(self, path_root: str = "base", sub_path: str = "save", original: Optional[Dict] = None) -> Dict:
        config_path = Path(self.get_path(path_root, sub_path))
        config_file = config_path.parent / "config.json"
        
        if config_file.exists():
            data = json.loads(config_file.read_text())
            return self._verify_and_merge_config(original, data)
        
        return original if original is not None else {}

    def delete_file(self, path_root: str = "base", relative_path: Optional[str] = None) -> bool:
        path = self.get_path(path_root, relative_path)
        if path and os.path.exists(path):
            try:
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    import shutil
                    shutil.rmtree(path)
                return True
            except Exception:
                return False
        return False

    def create_temp_txt(self, content: str = "") -> str:
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
        temp_file.write(content)
        temp_file.close()
        self._temp_files.append(temp_file.name)
        return temp_file.name

    def get_temp_files(self) -> List[str]:
        return self._temp_files.copy()

    def get_last_temp_file(self) -> Optional[str]:
        if self._temp_files:
            return self._temp_files[-1]
        return None

    def get_latest_version(self) -> Optional[str]:
        version_file = Path(self.get_base_path()) / "version.txt"
        if version_file.exists():
            return version_file.read_text().strip()
        return None