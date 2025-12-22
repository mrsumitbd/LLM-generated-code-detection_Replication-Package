from typing import Optional, Dict, List

class StorageManager:

    def __init__(self):
        pass

    def get_executable_path(self) -> str:
        pass

    def get_base_path(self) -> str:
        pass

    def is_frozen(self) -> bool:
        pass

    def is_running_from_source(self) -> bool:
        pass

    def _verify_and_merge_config(self, original: Optional[Dict], new_data: Optional[Dict]) -> Dict:
        pass

    def _generate_key(self, path_root: str = "base", sub_path: str = "save") -> None:
        pass

    def _load_key(self, path_root: str = "base", sub_path: str = "save") -> Optional[bytes]:
        pass

    def get_path(self, path_root: str = "base", relative_path: Optional[str] = None) -> Optional[str]:
        pass

    def get_existing_path(self, path_root: str = "base", relative_path: Optional[str] = None) -> Optional[str]:
        pass

    def save_config(self, path_root: str = "base", sub_path: str = "save", new: Optional[Dict] = None, original: Optional[Dict] = None) -> None:
        pass

    def load_config(self, path_root: str = "base", sub_path: str = "save", original: Optional[Dict] = None) -> Dict:
        pass

    def delete_file(self, path_root: str = "base", relative_path: Optional[str] = None) -> bool:
        pass

    def create_temp_txt(self, content: str = "") -> str:
        pass

    def get_temp_files(self) -> List[str]:
        pass

    def get_last_temp_file(self) -> Optional[str]:
        pass

    def get_latest_version(self) -> Optional[str]:
        pass