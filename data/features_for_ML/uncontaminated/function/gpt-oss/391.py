import argparse
import difflib
import os
import pathlib
import sys
from typing import Iterable, Tuple


def _read_text(path: pathlib.Path) -> str:
    """Read a file as text, using UTF‑8 with a fallback to latin‑1."""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1")


def _compare_files(file1: pathlib.Path, file2: pathlib.Path) -> int:
    """Compare two files. Return 0 if identical, 1 otherwise."""
    if file1.stat().st_size != file2.stat().st_size:
        print(f"Size differs: {file1} ({file1.stat().st_size} bytes) "
              f"vs {file2} ({file2.stat().st_size} bytes)")
        return 1

    # Compare byte by byte for speed
    with file1.open("rb") as f1, file2.open("rb") as f2:
        while True:
            b1 = f1.read(8192)
            b2 = f2.read(8192)
            if not b1 and not b2:
                break
            if b1 != b2:
                # Fallback to text diff for readability
                txt1 = _read_text(file1)
                txt2 = _read_text(file2)
                diff = difflib.unified_diff(
                    txt1.splitlines(),
                    txt2.splitlines(),
                    fromfile=str(file1),
                    tofile=str(file2),
                    lineterm="",
                )
                print("\n".join(diff))
                return 1
    return 0


def _walk_dir(root: pathlib.Path) -> Iterable[Tuple[pathlib.Path, pathlib.Path]]:
    """Yield (relative_path, absolute_path) for all files under root."""
    for path in root.rglob("*"):
        if path.is_file():
            yield (path.relative_to(root), path)


def _compare_dirs(dir1: pathlib.Path, dir2: pathlib.Path) -> int:
    """Recursively compare two directories. Return 0 if identical, 1 otherwise."""
    files1 = {rel: abs_path for rel, abs_path in _walk_dir(dir1)}
    files2 = {rel: abs_path for rel, abs_path in _walk_dir(dir2)}

    all_keys = set(files1) | set(files2)
    status = 0

    for key in sorted(all_keys):
        p1 = files1.get(key)
        p2 = files2.get(key)

        if p1 is None:
            print(f"Only in {dir2}: {key}")
            status = 1
            continue
        if p2 is None:
            print(f"Only in {dir1}: {key}")
            status = 1
            continue

        # Both exist, compare files
        if _compare_files(p1, p2) != 0:
            status = 1

    return status


def compare(args: argparse.Namespace) -> int:
    """
    Compare two files or directories specified in args.

    Expected arguments:
        file1: Path to first file or directory.
        file2: Path to second file or directory.
    """
    path1 = pathlib.Path(args.file1)
    path2 = pathlib.Path(args.file2)

    if not path1.exists():
        print(f"Error: {path1} does not exist.", file=sys.stderr)
        return 1
    if not path2.exists():
        print(f"Error: {path2} does not exist.", file=sys.stderr)
        return 1

    if path1.is_file() and path2.is_file():
        return _compare_files(path1, path2)

    if path1.is_dir() and path2.is_dir():
        return _compare_dirs(path1, path2)

    print(
        f"Error: both arguments must refer to files or directories of the same type.",
        file=sys.stderr,
    )
    return 1