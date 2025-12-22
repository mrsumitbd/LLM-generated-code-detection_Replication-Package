from pathlib import Path
import mmap
import blake3

def _blake3(file_path: Path) -> str:
    """Hashes a file using BLAKE3, using parallelized and memory-mapped I/O to avoid reading the entire file into memory.

    Args:
        file_path: Path to the file to hash

    Returns:
        Hexdigest of the hash of the file
    """
    # Ensure the path is a Path object
    if not isinstance(file_path, Path):
        file_path = Path(file_path)

    # Open the file in binary mode and memory-map it
    with file_path.open("rb") as f:
        # Map the entire file into memory (read-only)
        mm = mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_READ)
        try:
            # Create a BLAKE3 hasher and feed the mmap buffer
            hasher = blake3.blake3()
            hasher.update(mm)
            # Return the hexadecimal digest
            return hasher.hexdigest()
        finally:
            mm.close()