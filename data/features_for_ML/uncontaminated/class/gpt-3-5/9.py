from typing import Union

class Book:

    def __init__(self, book_dir: str, file_path: str):
        self.book_dir = book_dir
        self.file_path = file_path

    def get_split_library(self) -> Union[dict[str, str], None]:
        pass

    def get_calibre_library(self) -> str:
        pass

    def get_time(self) -> str:
        pass

    def get_title_and_author(self) -> tuple[str, str, str]:
        pass

    def get_new_metadata_path(self) -> str:
        pass

    def export_as_dict(self) -> dict[str, Union[str, None]]:
        pass