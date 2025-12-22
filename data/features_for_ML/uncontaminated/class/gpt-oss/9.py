import os
import json
import datetime
from pathlib import Path
from typing import Optional, Tuple, Dict, Union


class Book:
    def __init__(self, book_dir: str, file_path: str):
        """
        Initialize a Book instance.

        :param book_dir: Directory where the book and its metadata are stored.
        :param file_path: Path to the book file.
        """
        self.book_dir = Path(book_dir).expanduser().resolve()
        self.file_path = Path(file_path).expanduser().resolve()
        self._split_library_cache: Optional[Dict[str, str]] = None
        self._calibre_library_cache: Optional[str] = None

    def get_split_library(self) -> Optional[Dict[str, str]]:
        """
        Load split library metadata from a JSON file named 'split_library.json'
        located in the book directory.

        :return: Dictionary of metadata if file exists, otherwise None.
        """
        if self._split_library_cache is not None:
            return self._split_library_cache

        split_lib_file = self.book_dir / "split_library.json"
        if not split_lib_file.is_file():
            return None

        try:
            with split_lib_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    self._split_library_cache = data
                    return data
        except Exception:
            pass

        return None

    def get_calibre_library(self) -> str:
        """
        Return the path to the Calibre library metadata file named
        'calibre_library.json' in the book directory. If the file does not
        exist, return an empty string.

        :return: Path to the Calibre library JSON file or empty string.
        """
        if self._calibre_library_cache is not None:
            return self._calibre_library_cache

        calibre_lib_file = self.book_dir / "calibre_library.json"
        if calibre_lib_file.is_file():
            self._calibre_library_cache = str(calibre_lib_file)
            return str(calibre_lib_file)

        self._calibre_library_cache = ""
        return ""

    def get_time(self) -> str:
        """
        Return the last modification time of the book file formatted as
        'YYYY-MM-DD HH:MM:SS'.

        :return: Formatted modification time string.
        """
        try:
            mtime = self.file_path.stat().st_mtime
            return datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            return ""

    def get_title_and_author(self) -> Tuple[str, str, str]:
        """
        Attempt to extract the title and author from the book file name.
        Expected format: 'Author - Title.ext' or 'Title.ext'.

        :return: Tuple containing (title, author, format).
        """
        name = self.file_path.stem  # filename without extension
        fmt = self.file_path.suffix.lstrip(".")
        author = ""
        title = name

        if " - " in name:
            parts = name.split(" - ", 1)
            if len(parts) == 2:
                author, title = parts[0].strip(), parts[1].strip()

        return title, author, fmt

    def get_new_metadata_path(self) -> str:
        """
        Construct a new metadata file path in the book directory with the
        same base name as the book file but with a '.json' extension.

        :return: Path to the new metadata JSON file.
        """
        new_meta = self.book_dir / f"{self.file_path.stem}.json"
        return str(new_meta)

    def export_as_dict(self) -> Dict[str, Union[str, None]]:
        """
        Export the book's metadata as a dictionary.

        :return: Dictionary containing title, author, format, time,
                 split_library, calibre_library, and new_metadata_path.
        """
        title, author, fmt = self.get_title_and_author()
        return {
            "title": title,
            "author": author,
            "format": fmt,
            "time": self.get_time(),
            "split_library": self.get_split_library(),
            "calibre_library": self.get_calibre_library(),
            "new_metadata_path": self.get_new_metadata_path(),
        }