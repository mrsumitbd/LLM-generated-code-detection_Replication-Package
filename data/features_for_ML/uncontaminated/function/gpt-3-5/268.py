from pathlib import Path
import blake3

def _blake3(file_path: Path) -> str:
    hasher = blake3.Blake3()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            hasher.update(chunk)
    return hasher.hexdigest()