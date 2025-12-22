import os
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional

class LibraryConverter:

    def __init__(self, args) -> None:
        self.args = args
        self.library_path = args.library_path if hasattr(args, 'library_path') else None
        self.backup_dir = args.backup_dir if hasattr(args, 'backup_dir') else None
        self.tmp_convert_dir = args.tmp_convert_dir if hasattr(args, 'tmp_convert_dir') else None
        self.ebook_convert_path = args.ebook_convert_path if hasattr(args, 'ebook_convert_path') else 'ebook-convert'
        self.books_to_convert = []
        self.library_structure = {}

    def get_split_library(self) -> dict[str, str] | None:
        if not self.library_path or not os.path.exists(self.library_path):
            return None
        
        split_library = {}
        for item in os.listdir(self.library_path):
            item_path = os.path.join(self.library_path, item)
            if os.path.isdir(item_path):
                split_library[item] = item_path
        
        return split_library if split_library else None

    def get_dirs(self, dirs_json_path: str) -> tuple[str, str, str]:
        if not os.path.exists(dirs_json_path):
            return "", "", ""
        
        try:
            with open(dirs_json_path, 'r') as f:
                dirs_data = json.load(f)
            
            library_path = dirs_data.get('library_path', '')
            backup_dir = dirs_data.get('backup_dir', '')
            tmp_convert_dir = dirs_data.get('tmp_convert_dir', '')
            
            return library_path, backup_dir, tmp_convert_dir
        except (json.JSONDecodeError, IOError):
            return "", "", ""

    def get_library_book_formats(self) -> dict[int, list[str]]:
        book_formats = {}
        book_id = 0
        
        if not self.library_path or not os.path.exists(self.library_path):
            return book_formats
        
        for book_dir in os.listdir(self.library_path):
            book_path = os.path.join(self.library_path, book_dir)
            if os.path.isdir(book_path):
                formats = []
                for file in os.listdir(book_path):
                    _, ext = os.path.splitext(file)
                    if ext:
                        formats.append(ext.lower().lstrip('.'))
                
                if formats:
                    book_formats[book_id] = formats
                    book_id += 1
        
        return book_formats

    def get_books_to_convert(self):
        self.books_to_convert = []
        
        if not self.library_path or not os.path.exists(self.library_path):
            return self.books_to_convert
        
        for book_dir in os.listdir(self.library_path):
            book_path = os.path.join(self.library_path, book_dir)
            if os.path.isdir(book_path):
                for file in os.listdir(book_path):
                    file_path = os.path.join(book_path, file)
                    _, ext = os.path.splitext(file)
                    if ext.lower() in ['.epub', '.pdf', '.mobi', '.azw', '.azw3']:
                        self.books_to_convert.append(file_path)
        
        return self.books_to_convert

    def backup(self, input_file, backup_type):
        if not self.backup_dir or not os.path.exists(input_file):
            return False
        
        os.makedirs(self.backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.basename(input_file)
        backup_filename = f"{backup_type}_{timestamp}_{filename}"
        backup_path = os.path.join(self.backup_dir, backup_filename)
        
        try:
            if os.path.isdir(input_file):
                shutil.copytree(input_file, backup_path)
            else:
                shutil.copy2(input_file, backup_path)
            return True
        except Exception:
            return False

    def convert_library(self):
        books = self.get_books_to_convert()
        
        for book_path in books:
            _, ext = os.path.splitext(book_path)
            import_format = ext.lower().lstrip('.')
            success, message = self.convert_to_kepub(book_path, import_format)
            
            if success:
                try:
                    os.remove(book_path)
                except Exception:
                    pass

    def convert_to_kepub(self, filepath: str, import_format: str) -> tuple[bool, str]:
        if not os.path.exists(filepath):
            return False, "File not found"
        
        os.makedirs(self.tmp_convert_dir, exist_ok=True)
        
        filename = os.path.basename(filepath)
        name_without_ext = os.path.splitext(filename)[0]
        output_file = os.path.join(self.tmp_convert_dir, f"{name_without_ext}.kepub.epub")
        
        try:
            cmd = [
                self.ebook_convert_path,
                filepath,
                output_file,
                '--output-profile=kobo'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0 and os.path.exists(output_file):
                original_dir = os.path.dirname(filepath)
                final_path = os.path.join(original_dir, f"{name_without_ext}.kepub.epub")
                shutil.move(output_file, final_path)
                return True, "Conversion successful"
            else:
                return False, result.stderr if result.stderr else "Conversion failed"
        except subprocess.TimeoutExpired:
            return False, "Conversion timeout"
        except Exception as e:
            return False, str(e)

    def empty_tmp_con_dir(self):
        if self.tmp_convert_dir and os.path.exists(self.tmp_convert_dir):
            try:
                shutil.rmtree(self.tmp_convert_dir)
                os.makedirs(self.tmp_convert_dir, exist_ok=True)
                return True
            except Exception:
                return False
        return False

    def set_library_permissions(self):
        if not self.library_path or not os.path.exists(self.library_path):
            return False
        
        try:
            for root, dirs, files in os.walk(self.library_path):
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    os.chmod(dir_path, 0o755)
                
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    os.chmod(file_path, 0o644)
            
            os.chmod(self.library_path, 0o755)
            return True
        except Exception:
            return False