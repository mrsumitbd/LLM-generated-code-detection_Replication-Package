import blake3
from pathlib import Path

def _blake3(file_path: Path) -> str:
    """Hashes a file using BLAKE3, using parallelized and memory-mapped I/O to avoid reading the entire file into memory.

    Args:
        file_path: Path to the file to hash

    Returns:
        Hexdigest of the hash of the file
    """
    hasher = blake3.blake3()
    with file_path.open('rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()