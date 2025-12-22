import json
import shutil
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Union

# Configure a basic logger for the module
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)


class Enforcer:
    """
    A helper class for managing a Calibre library, enforcing cover images,
    handling metadata, and working with log files.
    """

    SUPPORTED_EXTENSIONS = {".epub", ".mobi", ".pdf", ".azw3", ".txt"}

    def __init__(self, args: Dict):
        """
        Initialise the Enforcer with a dictionary of arguments.

        Expected keys (optional):
            - library_path: Path to the Calibre library root.
            - log_path: Path to the log file.
            - metadata_temp: Path to a temporary metadata directory.
        """
        self.args = args
        self.library_path = Path(args.get("library_path", Path.home() / "Calibre Library")).resolve()
        self.log_path = Path(args.get("log_path", self.library_path / "calibre_log.json")).resolve()
        self.metadata_temp = Path(args.get("metadata_temp", Path.home() / ".metadata_temp")).resolve()

        # Ensure directories exist
        self.library_path.mkdir(parents=True, exist_ok=True)
        self.metadata_temp.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Library and log utilities
    # ------------------------------------------------------------------
    def get_calibre_library(self) -> str:
        """Return the absolute path to the Calibre library."""
        return str(self.library_path)

    def read_log(self, auto: bool = True, log_path: str = "None") -> Dict:
        """
        Read the log file and return its contents as a dictionary.

        Parameters
        ----------
        auto : bool
            If True, use the default log path set during initialisation.
        log_path : str
            Override path to the log file. If "None", the default is used.
        """
        path = Path(log_path) if log_path != "None" else self.log_path
        if not path.is_file():
            log.warning(f"Log file not found: {path}")
            return {}
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            log.info(f"Read log file: {path}")
            return data
        except Exception as exc:
            log.error(f"Failed to read log file {path}: {exc}")
            return {}

    def get_book_dir_from_log(self, log_info: Dict) -> str:
        """
        Extract the book directory path from a log entry.

        Parameters
        ----------
        log_info : dict
            A dictionary containing log information. Expected to have a
            'book_dir' key.

        Returns
        -------
        str
            The book directory path, or an empty string if not found.
        """
        book_dir = log_info.get("book_dir", "")
        if book_dir:
            log.info(f"Book directory from log: {book_dir}")
        else:
            log.warning("No 'book_dir' key found in log entry.")
        return book_dir

    # ------------------------------------------------------------------
    # File handling
    # ------------------------------------------------------------------
    def get_supported_files_from_dir(self, dir: str) -> List[str]:
        """
        Return a list of supported file names in the given directory.

        Parameters
        ----------
        dir : str
            Path to the directory to scan.

        Returns
        -------
        list[str]
            List of file names with supported extensions.
        """
        path = Path(dir)
        if not path.is_dir():
            log.warning(f"Directory does not exist: {dir}")
            return []

        files = [
            f.name
            for f in path.iterdir()
            if f.is_file() and f.suffix.lower() in self.SUPPORTED_EXTENSIONS
        ]
        log.info(f"Found {len(files)} supported files in {dir}")
        return files

    def enforce_cover(self, book_dir: str) -> List[str]:
        """
        Ensure that a cover image exists in the book directory.

        Parameters
        ----------
        book_dir : str
            Path to the book directory.

        Returns
        -------
        list
            List of actions performed (e.g., copied cover image).
        """
        actions = []
        book_path = Path(book_dir)
        if not book_path.is_dir():
            log.warning(f"Book directory not found: {book_dir}")
            return actions

        # Look for common cover filenames
        cover_candidates = ["cover.jpg", "cover.png", "cover.jpeg"]
        cover_src = None
        for name in cover_candidates:
            candidate = book_path / name
            if candidate.is_file():
                cover_src = candidate
                break

        if not cover_src:
            log.info(f"No cover image found in {book_dir}")
            return actions

        # Destination cover image
        dest_cover = book_path / "cover.jpg"
        try:
            shutil.copy2(cover_src, dest_cover)
            actions.append(f"Copied {cover_src} to {dest_cover}")
            log.info(f"Copied cover image to {dest_cover}")
        except Exception as exc:
            log.error(f"Failed to copy cover image: {exc}")

        return actions

    def enforce_all_covers(self) -> Union[Tuple[int, float, int], Tuple[bool, bool, bool]]:
        """
        Enforce cover images for all books in the library.

        Returns
        -------
        tuple
            If successful: (total_books, success_rate, failures)
            If an error occurs: (False, False, False)
        """
        try:
            book_dirs = [p for p in self.library_path.iterdir() if p.is_dir()]
            total = len(book_dirs)
            successes = 0
            failures = 0

            for book_dir in book_dirs:
                actions = self.enforce_cover(str(book_dir))
                if actions:
                    successes += 1
                else:
                    failures += 1

            success_rate = successes / total if total else 0.0
            log.info(f"Enforced covers: {successes}/{total} successes, {failures} failures")
            return total, success_rate, failures
        except Exception as exc:
            log.error(f"Error enforcing covers: {exc}")
            return False, False, False

    # ------------------------------------------------------------------
    # Metadata handling
    # ------------------------------------------------------------------
    def replace_old_metadata(self, old_metadata: str, new_metadata: str) -> None:
        """
        Replace the contents of an old metadata file with new metadata.

        Parameters
        ----------
        old_metadata : str
            Path to the old metadata file.
        new_metadata : str
            Path to the new metadata file.
        """
        old_path = Path(old_metadata)
        new_path = Path(new_metadata)

        if not old_path.is_file():
            log.warning(f"Old metadata file not found: {old_metadata}")
            return
        if not new_path.is_file():
            log.warning(f"New metadata file not found: {new_metadata}")
            return

        try:
            shutil.copy2(new_path, old_path)
            log.info(f"Replaced {old_metadata} with {new_metadata}")
        except Exception as exc:
            log.error(f"Failed to replace metadata: {exc}")

    def print_library_list(self) -> None:
        """Print the names of all books (subdirectories) in the library."""
        book_dirs = [p.name for p in self.library_path.iterdir() if p.is_dir()]
        if not book_dirs:
            log.info("No books found in the library.")
            return
        log.info("Books in library:")
        for name in book_dirs:
            print(f" - {name}")

    # ------------------------------------------------------------------
    # Log and temp file utilities
    # ------------------------------------------------------------------
    def delete_log(self, auto: bool = True, log_path: str = "None") -> None:
        """
        Delete the log file.

        Parameters
        ----------
        auto : bool
            If True, delete the default log file.
        log_path : str
            Override path to the log file. If "None", the default is used.
        """
        path = Path(log_path) if log_path != "None" else self.log_path
        try:
            if path.is_file():
                path.unlink()
                log.info(f"Deleted log file: {path}")
            else:
                log.warning(f"Log file does not exist: {path}")
        except Exception as exc:
            log.error(f"Failed to delete log file {path}: {exc}")

    def empty_metadata_temp(self) -> None:
        """Remove all files in the temporary metadata directory."""
        try:
            for item in self.metadata_temp.iterdir():
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
            log.info(f"Emptied metadata temp directory: {self.metadata_temp}")
        except Exception as exc:
            log.error(f"Failed to empty metadata temp: {exc}")

    def check_for_other_logs(self) -> List[str]:
        """
        Return a list of other log files in the library directory.

        Returns
        -------
        list[str]
            Paths to other log files (excluding the main log file).
        """
        logs = []
        try:
            for item in self.library_path.iterdir():
                if item.is_file() and item.suffix.lower() == ".json" and item != self.log_path:
                    logs.append(str(item))
            log.info(f"Found {len(logs)} other log files.")
        except Exception as exc:
            log.error(f"Error checking for other logs: {exc}")
        return logs