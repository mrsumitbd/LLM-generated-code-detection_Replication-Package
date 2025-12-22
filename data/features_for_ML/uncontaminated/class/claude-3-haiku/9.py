import os
import re
from datetime import datetime

class Book:
    def __init__(self, book_dir: str, file_path: str):
        self.book_dir = book_dir
        self.file_path = file_path

    def get_split_library(self) -> dict[str, str] | None:
        try:
            split_library = {}
            for root, dirs, files in os.walk(self.book_dir):
                for file in files:
                    if file.endswith(".epub") or file.endswith(".mobi"):
                        file_path = os.path.join(root, file)
                        author = self.get_author_from_path(file_path)
                        split_library[author] = file_path
            return split_library
        except (OSError, ValueError):
            return None

    def get_calibre_library(self) -> str:
        return os.path.dirname(self.file_path)

    def get_time(self) -> str:
        return datetime.fromtimestamp(os.path.getmtime(self.file_path)).strftime('%Y-%m-%d %H:%M:%S')

    def get_title_and_author(self) -> tuple[str, str, str]:
        title = os.path.splitext(os.path.basename(self.file_path))[0]
        author = self.get_author_from_path(self.file_path)
        return title, author, self.file_path

    def get_new_metadata_path(self) -> str:
        return os.path.join(self.book_dir, f"{self.get_title_and_author()[0]}.json")

    def export_as_dict(self) -> dict[str, str | None]:
        return {
            "title": self.get_title_and_author()[0],
            "author": self.get_title_and_author()[1],
            "file_path": self.file_path,
            "calibre_library": self.get_calibre_library(),
            "modified_time": self.get_time(),
            "new_metadata_path": self.get_new_metadata_path(),
            "split_library": str(self.get_split_library())
        }

    def get_author_from_path(self, file_path: str) -> str:
        author_pattern = r"[/\\]([^/\\]+)[/\\]"
        match = re.search(author_pattern, file_path)
        if match:
            return match.group(1)
        else:
            return "Unknown"