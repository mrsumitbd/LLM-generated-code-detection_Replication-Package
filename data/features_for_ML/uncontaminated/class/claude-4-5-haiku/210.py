import os
import json
import time
from pathlib import Path
from datetime import datetime

class Enforcer:

    def __init__(self, args):
        self.args = args
        self.calibre_library = None
        self.metadata_temp_dir = os.path.join(os.path.expanduser("~"), ".enforcer_metadata_temp")
        self._ensure_temp_dir()

    def _ensure_temp_dir(self):
        os.makedirs(self.metadata_temp_dir, exist_ok=True)

    def get_calibre_library(self) -> str:
        if self.calibre_library:
            return self.calibre_library
        
        calibre_config = os.path.join(os.path.expanduser("~"), ".calibre")
        metadata_db = os.path.join(calibre_config, "metadata.db")
        
        if os.path.exists(metadata_db):
            with open(os.path.join(calibre_config, "library_path.txt"), "r") as f:
                self.calibre_library = f.read().strip()
                return self.calibre_library
        
        return ""

    def read_log(self, auto=True, log_path: str = "None") -> dict:
        if log_path == "None":
            log_path = os.path.join(os.path.expanduser("~"), ".enforcer_log.json")
        
        if not os.path.exists(log_path):
            return {}
        
        try:
            with open(log_path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def get_book_dir_from_log(self, log_info: dict) -> str:
        if "book_dir" in log_info:
            return log_info["book_dir"]
        return ""

    def get_supported_files_from_dir(self, dir: str) -> list[str]:
        supported_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"}
        supported_files = []
        
        if not os.path.isdir(dir):
            return supported_files
        
        for file in os.listdir(dir):
            if os.path.splitext(file)[1].lower() in supported_extensions:
                supported_files.append(os.path.join(dir, file))
        
        return supported_files

    def enforce_cover(self, book_dir: str) -> list:
        if not os.path.isdir(book_dir):
            return []
        
        cover_files = []
        for file in os.listdir(book_dir):
            if file.lower() in ["cover.jpg", "cover.jpeg", "cover.png"]:
                cover_files.append(os.path.join(book_dir, file))
        
        return cover_files

    def enforce_all_covers(self) -> tuple[int, float, int] | tuple[bool, bool, bool]:
        library = self.get_calibre_library()
        if not library:
            return (False, False, False)
        
        total_books = 0
        total_time = 0.0
        successful = 0
        
        start_time = time.time()
        
        for book_folder in os.listdir(library):
            book_path = os.path.join(library, book_folder)
            if os.path.isdir(book_path):
                total_books += 1
                covers = self.enforce_cover(book_path)
                if covers:
                    successful += 1
        
        total_time = time.time() - start_time
        
        return (total_books, total_time, successful)

    def replace_old_metadata(self, old_metadata: str, new_metadata: str) -> None:
        old_path = os.path.join(self.metadata_temp_dir, old_metadata)
        new_path = os.path.join(self.metadata_temp_dir, new_metadata)
        
        if os.path.exists(old_path):
            os.remove(old_path)
        
        if os.path.exists(new_path):
            pass

    def print_library_list(self) -> None:
        library = self.get_calibre_library()
        if not library or not os.path.isdir(library):
            print("No Calibre library found")
            return
        
        books = [d for d in os.listdir(library) if os.path.isdir(os.path.join(library, d))]
        for book in sorted(books):
            print(book)

    def delete_log(self, auto=True, log_path="None"):
        if log_path == "None":
            log_path = os.path.join(os.path.expanduser("~"), ".enforcer_log.json")
        
        if os.path.exists(log_path):
            os.remove(log_path)

    def empty_metadata_temp(self):
        if os.path.exists(self.metadata_temp_dir):
            for file in os.listdir(self.metadata_temp_dir):
                file_path = os.path.join(self.metadata_temp_dir, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)

    def check_for_other_logs(self):
        home_dir = os.path.expanduser("~")
        log_files = []
        
        for file in os.listdir(home_dir):
            if file.startswith(".enforcer") and file.endswith(".json"):
                log_files.append(os.path.join(home_dir, file))
        
        return log_files