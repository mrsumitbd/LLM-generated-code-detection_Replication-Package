import os
from pathlib import Path
from typing import List

def load_book_content(setup: str, data_dir: str) -> str:
    """
    Load the content of a book from the given data directory.

    Parameters
    ----------
    setup : str
        The name of the book file or directory. If it is a file name, the
        function will read that file. If it is a directory name, the
        function will read all .txt files inside that directory in
        lexicographical order and concatenate them.

    data_dir : str
        The root directory where book files or directories are located.

    Returns
    -------
    str
        The full text content of the book.

    Raises
    ------
    FileNotFoundError
        If the specified file or directory does not exist.
    """
    base_path = Path(data_dir).expanduser().resolve()
    target = base_path / setup

    if not target.exists():
        raise FileNotFoundError(f"'{target}' does not exist")

    # If target is a file, read and return its content
    if target.is_file():
        return target.read_text(encoding="utf-8")

    # If target is a directory, read all .txt files sorted by name
    if target.is_dir():
        txt_files: List[Path] = sorted(
            [p for p in target.iterdir() if p.is_file() and p.suffix.lower() == ".txt"]
        )
        if not txt_files:
            raise FileNotFoundError(f"No .txt files found in directory '{target}'")
        contents = []
        for txt_file in txt_files:
            contents.append(txt_file.read_text(encoding="utf-8"))
        return "\n".join(contents)

    # If target is neither file nor directory (unlikely), raise an error
    raise FileNotFoundError(f"Unsupported file type for '{target}'")