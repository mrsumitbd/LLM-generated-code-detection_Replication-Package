from typing import List, Dict, Tuple

class LibraryConverter:

    def __init__(self, args) -> None:
        pass

    def get_split_library(self) -> Dict[str, str] | None:
        pass

    def get_dirs(self, dirs_json_path: str) -> Tuple[str, str, str]:
        pass

    def get_library_book_formats(self) -> Dict[int, List[str]]:
        pass

    def get_books_to_convert(self):
        pass

    def backup(self, input_file, backup_type):
        pass

    def convert_library(self):
        pass

    def convert_to_kepub(self, filepath:str ,import_format:str) -> Tuple[bool, str]:
        pass

    def empty_tmp_con_dir(self):
        pass

    def set_library_permissions(self):
        pass