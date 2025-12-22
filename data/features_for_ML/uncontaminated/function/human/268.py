from pathlib import Path
from blake3 import blake3

def _blake3(file_path: Path) -> str:
        """Hashes a file using BLAKE3, using parallelized and memory-mapped I/O to avoid reading the entire file into memory.

        Args:
            file_path: Path to the file to hash

        Returns:
            Hexdigest of the hash of the file
        """
        file_hasher = blake3(max_threads=blake3.AUTO)
        file_hasher.update_mmap(file_path)
        return file_hasher.hexdigest()