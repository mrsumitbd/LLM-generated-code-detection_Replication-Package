import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Iterable


class LibraryConverter:
    """
    A utility class for converting e‑book files in a library to a target format
    (e.g. kepub).  The class expects a configuration dictionary passed to the
    constructor.  The configuration keys are:

        * library_path   – Path to the root of the library.
        * tmp_dir        – Temporary directory used during conversion.
        * backup_dir     – Directory where original files are backed up.
        * target_format  – Desired output format (e.g. "kepub").
        * formats        – List of supported input formats (e.g. ["epub", "mobi"]).
        * dirs_json_path – Optional JSON file that contains a mapping of
                           directory names to absolute paths.

    The class is intentionally lightweight and does not depend on external
    libraries beyond the standard library and Calibre's `ebook-convert`
    command line tool.
    """

    def __init__(self, args: Dict[str, str]) -> None:
        self.args = args
        self.library_path = Path(args.get("library_path", ".")).expanduser().resolve()
        self.tmp_dir = Path(args.get("tmp_dir", "./tmp")).expanduser().resolve()
        self.backup_dir = Path(args.get("backup_dir", "./backup")).expanduser().resolve()
        self.target_format = args.get("target_format", "kepub").lower()
        self.supported_formats = [
            f.lower().lstrip(".") for f in args.get("formats", ["epub", "mobi"])
        ]
        self.dirs_json_path = args.get("dirs_json_path")

        # Ensure directories exist
        self.tmp_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------------------- #
    #  Directory helpers
    # --------------------------------------------------------------------- #
    def get_split_library(self) -> Optional[Dict[str, str]]:
        """
        Return a mapping of sub‑library names to absolute paths if the library
        is split into multiple sub‑directories.  The method looks for a file
        named `split_library.json` in the library root.  If the file does not
        exist, None is returned.
        """
        split_file = self.library_path / "split_library.json"
        if not split_file.is_file():
            return None
        try:
            with split_file.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
            # Ensure all paths are absolute
            return {k: str(Path(v).expanduser().resolve()) for k, v in data.items()}
        except Exception:
            return None

    def get_dirs(self, dirs_json_path: str) -> Tuple[str, str, str]:
        """
        Load a JSON file that contains three directory paths:
            {"library": "...", "tmp": "...", "backup": "..."}
        The method returns a tuple of absolute paths in the order
        (library, tmp, backup).  If the file is missing or malformed,
        the constructor defaults are used.
        """
        path = Path(dirs_json_path).expanduser().resolve()
        if not path.is_file():
            return (
                str(self.library_path),
                str(self.tmp_dir),
                str(self.backup_dir),
            )
        try:
            with path.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
            lib = Path(data.get("library", self.library_path)).expanduser().resolve()
            tmp = Path(data.get("tmp", self.tmp_dir)).expanduser().resolve()
            bak = Path(data.get("backup", self.backup_dir)).expanduser().resolve()
            return (str(lib), str(tmp), str(bak))
        except Exception:
            return (
                str(self.library_path),
                str(self.tmp_dir),
                str(self.backup_dir),
            )

    # --------------------------------------------------------------------- #
    #  Library scanning
    # --------------------------------------------------------------------- #
    def get_library_book_formats(self) -> Dict[int, List[str]]:
        """
        Scan the library directory for e‑book files and return a mapping
        from a numeric book ID (derived from the file name) to a list of
        detected formats.  Files that do not match the supported formats
        are ignored.
        """
        book_formats: Dict[int, List[str]] = {}
        for root, _, files in os.walk(self.library_path):
            for fname in files:
                ext = Path(fname).suffix.lower().lstrip(".")
                if ext not in self.supported_formats:
                    continue
                try:
                    # Assume the file name starts with an integer ID
                    book_id = int(Path(fname).stem.split("_")[0])
                except ValueError:
                    continue
                book_formats.setdefault(book_id, []).append(ext)
        return book_formats

    def get_books_to_convert(self) -> Iterable[Tuple[int, Path]]:
        """
        Yield tuples of (book_id, Path) for each book that does not already
        contain the target format.  The path returned is the path to the
        first available source file for that book.
        """
        book_formats = self.get_library_book_formats()
        for book_id, formats in book_formats.items():
            if self.target_format in formats:
                continue
            # Find the first file for this book
            for root, _, files in os.walk(self.library_path):
                for fname in files:
                    if fname.lower().startswith(f"{book_id}_") and fname.lower().endswith(
                        f".{self.target_format}"
                    ):
                        continue
                    if fname.lower().startswith(f"{book_id}_") and Path(fname).suffix.lower().lstrip(".") in formats:
                        yield book_id, Path(root) / fname
                        break

    # --------------------------------------------------------------------- #
    #  Backup and permissions
    # --------------------------------------------------------------------- #
    def backup(self, input_file: Path, backup_type: str = "original") -> Path:
        """
        Create a backup copy of *input_file* in the backup directory.
        The backup file name is constructed as:
            <original_name>.<backup_type>.<timestamp>
        The method returns the Path to the backup file.
        """
        timestamp = Path(input_file).stem + f".{backup_type}.{int(os.path.getmtime(input_file))}"
        backup_path = self.backup_dir / f"{input_file.name}.{backup_type}.{int(os.path.getmtime(input_file))}"
        shutil.copy2(input_file, backup_path)
        return backup_path

    def set_library_permissions(self) -> None:
        """
        Recursively set read/write/execute permissions for the library
        directory to 0o755 for directories and 0o644 for files.
        """
        for root, dirs, files in os.walk(self.library_path):
            for d in dirs:
                os.chmod(Path(root) / d, 0o755)
            for f in files:
                os.chmod(Path(root) / f, 0o644)

    # --------------------------------------------------------------------- #
    #  Conversion helpers
    # --------------------------------------------------------------------- #
    def empty_tmp_con_dir(self) -> None:
        """
        Remove all files and sub‑directories in the temporary conversion
        directory.
        """
        if not self.tmp_dir.is_dir():
            return
        for item in self.tmp_dir.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()

    def convert_to_kepub(self, filepath: Path, import_format: str) -> Tuple[bool, str]:
        """
        Convert *filepath* to the target format using Calibre's
        `ebook-convert` command.  The output file is written to the temporary
        directory.  The method returns a tuple (success, message) where
        *success* is True if the conversion succeeded and *message* contains
        either the path to the converted file or an error message.
        """
        output_file = self.tmp_dir / f"{filepath.stem}.{self.target_format}"
        cmd = [
            "ebook-convert",
            str(filepath),
            str(output_file),
            "--output-profile",
            "kepubify",
        ]
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
            )
            return True, str(output_file)
        except subprocess.CalledProcessError as exc:
            return False, f"Conversion failed: {exc.stderr.strip()}"
        except FileNotFoundError:
            return False, "ebook-convert not found in PATH"

    # --------------------------------------------------------------------- #
    #  Main conversion routine
    # --------------------------------------------------------------------- #
    def convert_library(self) -> None:
        """
        Main entry point for converting the entire library.  The method
        iterates over all books that need conversion, backs up the original
        file, performs the conversion, and replaces the original with the
        converted file.  Errors are logged to the console but do not stop
        the conversion of other books.
        """
        self.empty_tmp_con_dir()
        for book_id, src_path in self.get_books_to_convert():
            print(f"Converting book {book_id}: {src_path.name}")
            backup_path = self.backup(src_path, "original")
            success, result = self.convert_to_kepub(src_path, src_path.suffix.lstrip("."))
            if not success:
                print(f"  ❌ {result}")
                continue
            try:
                shutil.move(result, src_path)
                print(f"  ✅ Converted and replaced {src_path.name}")
            except Exception as exc:
                print(f"  ❌ Failed to replace original: {exc}")
                # Restore backup
                shutil.move(backup_path, src_path)
        self.set_library_permissions()