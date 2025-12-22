import os
import shutil
import json
from typing import Tuple, Dict, List
from subprocess import Popen, PIPE

class LibraryConverter:
    def __init__(self, args) -> None:
        self.args = args
        self.tmp_con_dir = os.path.join(self.args.tmp_dir, 'converted')
        self.tmp_backup_dir = os.path.join(self.args.tmp_dir, 'backup')

    def get_split_library(self) -> Dict[str, str] | None:
        if os.path.exists(self.args.split_library_path):
            with open(self.args.split_library_path, 'r') as f:
                return json.load(f)
        return None

    def get_dirs(self, dirs_json_path: str) -> Tuple[str, str, str]:
        with open(dirs_json_path, 'r') as f:
            dirs = json.load(f)
        return dirs['library_dir'], dirs['tmp_dir'], dirs['backup_dir']

    def get_library_book_formats(self) -> Dict[int, List[str]]:
        book_formats = {}
        for root, dirs, files in os.walk(self.args.library_dir):
            for file in files:
                ext = os.path.splitext(file)[1][1:].lower()
                if ext in self.args.supported_formats:
                    book_id = int(os.path.splitext(file)[0])
                    if book_id not in book_formats:
                        book_formats[book_id] = []
                    book_formats[book_id].append(ext)
        return book_formats

    def get_books_to_convert(self):
        books_to_convert = []
        split_library = self.get_split_library()
        if split_library:
            for book_id, formats in self.get_library_book_formats().items():
                if str(book_id) in split_library and 'kepub' not in formats:
                    books_to_convert.append(book_id)
        else:
            for book_id, formats in self.get_library_book_formats().items():
                if 'kepub' not in formats:
                    books_to_convert.append(book_id)
        return books_to_convert

    def backup(self, input_file, backup_type):
        backup_dir = self.tmp_backup_dir if backup_type == 'tmp' else self.args.backup_dir
        backup_path = os.path.join(backup_dir, os.path.basename(input_file))
        shutil.copy2(input_file, backup_path)

    def convert_library(self):
        books_to_convert = self.get_books_to_convert()
        for book_id in books_to_convert:
            for format in self.get_library_book_formats()[book_id]:
                input_file = os.path.join(self.args.library_dir, f"{book_id}.{format}")
                self.backup(input_file, 'tmp')
                self.convert_to_kepub(input_file, format)
        self.set_library_permissions()

    def convert_to_kepub(self, filepath: str, import_format: str) -> Tuple[bool, str]:
        output_file = os.path.join(self.tmp_con_dir, os.path.basename(filepath))
        output_file = os.path.splitext(output_file)[0] + '.kepub.epub'
        cmd = ['ebook-convert', filepath, output_file, f'--input-format={import_format}', '--output-format=kepub']
        process = Popen(cmd, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            return True, output_file
        return False, stderr.decode()

    def empty_tmp_con_dir(self):
        if os.path.exists(self.tmp_con_dir):
            shutil.rmtree(self.tmp_con_dir)
        os.makedirs(self.tmp_con_dir)

    def set_library_permissions(self):
        os.chmod(self.args.library_dir, 0o755)
        for root, dirs, files in os.walk(self.args.library_dir):
            for d in dirs:
                os.chmod(os.path.join(root, d), 0o755)
            for f in files:
                os.chmod(os.path.join(root, f), 0o644)