import json
import os
import subprocess
import time
from datetime import datetime
from acw_db import ACW_DB

class Enforcer:
    def __init__(self, args):
        self.db = ACW_DB()
        self.acw_settings = self.db.acw_settings
        self.enforcer_on = self.acw_settings["auto_metadata_enforcement"]
        self.supported_formats = ["epub", "azw3"]

        self.args = args
        self.calibre_library = self.get_calibre_library()
        self.calibre_env = os.environ.copy()
        self.calibre_env["HOME"] = os.environ.get("ACW_CONFIG_DIR", "/config")

        self.illegal_characters = ["<", ">", ":", '"', "/", "\\", "|", "?", "*"]

    def get_calibre_library(self) -> str:
        """Gets Calibre-Library location from dirs_json path"""
        with open(dirs_json, "r") as f:
            dirs = json.load(f)
        return dirs["calibre_library_dir"]  # Returns without / on the end

    def read_log(self, auto=True, log_path: str = "None") -> dict:
        """Reads pertinent information from the given log file, adds the book_id from the log name and returns the info as a dict"""
        if auto:
            book_id = (self.args.log.split("-")[1]).split(".")[0]
            timestamp_raw = self.args.log.split("-")[0]
            timestamp = datetime.strptime(timestamp_raw, "%Y%m%d%H%M%S")

            log_info = {}
            with open(f"{change_logs_dir}/{self.args.log}", "r") as f:
                log_info = json.load(f)
            log_info["book_id"] = book_id
            log_info["timestamp"] = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        else:
            log_name = os.path.basename(log_path)
            book_id = (log_name.split("-")[1]).split(".")[0]
            timestamp_raw = log_name.split("-")[0]
            timestamp = datetime.strptime(timestamp_raw, "%Y%m%d%H%M%S")

            log_info = {}
            with open(log_path, "r") as f:
                log_info = json.load(f)
            log_info["book_id"] = book_id
            log_info["timestamp"] = timestamp.strftime("%Y-%m-%d %H:%M:%S")

        return log_info

    def get_book_dir_from_log(self, log_info: dict) -> str:
        book_title = log_info["title"].replace(":", "_")
        author_name = (log_info["authors"].split(", ")[0]).split(" & ")[0]
        book_id = log_info["book_id"]

        for char in book_title:
            if char in self.illegal_characters:
                book_title = book_title.replace(char, "_")
        for char in author_name:
            if char in self.illegal_characters:
                author_name = author_name.replace(char, "_")

        book_dir = f"{self.calibre_library}/{author_name}/{book_title} ({book_id})/"
        log_info["file_path"] = book_dir

        return book_dir

    def get_supported_files_from_dir(self, dir: str) -> list[str]:
        """Returns a list if the book dir given contains files of one or more of the supported formats"""
        library_files = [
            os.path.join(dirpath, f)
            for (dirpath, dirnames, filenames) in os.walk(dir)
            for f in filenames
        ]

        supported_files = []
        for format in self.supported_formats:
            supported_files = supported_files + [
                f for f in library_files if f.endswith(f".{format}")
            ]

        return supported_files

    def enforce_cover(self, book_dir: str) -> list:
        """Will force the Cover & Metadata to update for the supported book files in the given directory"""
        supported_files = self.get_supported_files_from_dir(book_dir)
        if supported_files:
            if len(supported_files) > 1:
                print(
                    "[cover-metadata-enforcer] Multiple file formats for current book detected...",
                    flush=True,
                )
            book_objects = []
            for file in supported_files:
                book = Book(book_dir, file)
                self.replace_old_metadata(
                    book.old_metadata_path, book.new_metadata_path
                )
                os.system(
                    f'ebook-polish -c "{book.cover_path}" -o "{book.new_metadata_path}" -U "{file}" "{file}"'
                )
                self.empty_metadata_temp()
                print(
                    f"[cover-metadata-enforcer]: DONE: '{book.title_author}.{book.file_format}': Cover & Metadata updated",
                    flush=True,
                )
                book_objects.append(book)

            return book_objects
        else:
            print(
                f"[cover-metadata-enforcer]: No supported file formats found in {book_dir}.",
                flush=True,
            )
            print(
                "[cover-metadata-enforcer]: *** NOTICE **** Only EPUB & AZW3 formats are currently supported.",
                flush=True,
            )
            return []

    def enforce_all_covers(self) -> tuple[int, float, int] | tuple[bool, bool, bool]:
        """Will force the covers and metadata to be re-generated for all books in the library"""
        t_start = time.time()

        supported_files = self.get_supported_files_from_dir(self.calibre_library)
        if supported_files:
            book_dirs = []
            for file in supported_files:
                book_dirs.append(os.path.dirname(file))

            print(
                f"[cover-metadata-enforcer]: {len(book_dirs)} books detected in Library"
            )
            print(
                f"[cover-metadata-enforcer]: Enforcing covers for {len(supported_files)} supported file(s) in {self.calibre_library} ..."
            )

            successful_enforcements = len(supported_files)

            for book_dir in book_dirs:
                try:
                    book_objects = self.enforce_cover(book_dir)
                    if book_objects:
                        book_dicts = []
                        for book in book_objects:
                            book_dicts.append(book.export_as_dict())
                        self.db.enforce_add_entry_from_all(book_dicts)
                except Exception as e:
                    print(f"[cover-metadata-enforcer]: ERROR: {book_dir}")
                    print(
                        f"[cover-metadata-enforcer]: Skipping book due to following error: {e}"
                    )
                    successful_enforcements = successful_enforcements - 1
                    continue

            t_end = time.time()

            return successful_enforcements, (t_end - t_start), len(supported_files)
        else:  # No supported files found
            return False, False, False

    def replace_old_metadata(self, old_metadata: str, new_metadata: str) -> None:
        """Switches the metadata in metadata_temp with the metadata in the Calibre-Library"""
        os.system(f'cp "{new_metadata}" "{old_metadata}"')

    def print_library_list(self) -> None:
        """Uses the calibredb command line utility to list the books in the library"""
        subprocess.run(
            ["calibredb", "list", "--with-library", self.calibre_library],
            env=self.calibre_env,
            check=True,
        )

    def delete_log(self, auto=True, log_path="None"):
        """Deletes the log file"""
        if auto:
            log = os.path.join(change_logs_dir, self.args.log)
            os.remove(log)
        else:
            os.remove(log_path)

    def empty_metadata_temp(self):
        """Empties the metadata_temp folder"""
        os.system(f"rm -r {metadata_temp_dir}/*")

    def check_for_other_logs(self):
        log_files = [
            os.path.join(dirpath, f)
            for (dirpath, dirnames, filenames) in os.walk(change_logs_dir)
            for f in filenames
        ]
        if len(log_files) > 0:
            print(
                f"[cover-metadata-enforcer] {len(log_files)} Additional metadata changes detected, processing now..",
                flush=True,
            )
            for log in log_files:
                if log.endswith(".json"):
                    log_info = self.read_log(auto=False, log_path=log)
                    book_dir = self.get_book_dir_from_log(log_info)
                    book_objects = self.enforce_cover(book_dir)
                    if book_objects:
                        for book in book_objects:
                            book.log_info = log_info
                            book.log_info["file_path"] = book.file_path
                            self.db.enforce_add_entry_from_log(book.log_info)
                    self.delete_log(auto=False, log_path=log)