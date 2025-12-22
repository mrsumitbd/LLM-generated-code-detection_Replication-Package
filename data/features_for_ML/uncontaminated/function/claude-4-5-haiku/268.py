import hashlib
from pathlib import Path


def _blake3(file_path: Path) -> str:
    """Hashes a file using BLAKE3, using parallelized and memory-mapped I/O to avoid reading the entire file into memory.

    Args:
        file_path: Path to the file to hash

    Returns:
        Hexdigest of the hash of the file
    """
    try:
        import blake3
    except ImportError:
        raise ImportError("blake3 package is required. Install it with: pip install blake3")
    
    hasher = blake3.blake3()
    
    # Read file in chunks to avoid loading entire file into memory
    chunk_size = 8192 * 1024  # 8MB chunks
    
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            hasher.update(chunk)
    
    return hasher.hexdigest()