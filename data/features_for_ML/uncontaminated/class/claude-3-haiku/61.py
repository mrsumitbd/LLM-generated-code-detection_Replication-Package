from pathlib import Path
from typing import Optional
import chardet

class EncodingManager:
    """Manages file encodings across multiple operations to ensure consistency."""

    def __init__(self, max_cache_size: Optional[int] = None):
        self.max_cache_size = max_cache_size
        self.encoding_cache = {}

    def detect_encoding(self, path: Path) -> str:
        if path in self.encoding_cache:
            return self.encoding_cache[path]

        with open(path, 'rb') as file:
            result = chardet.detect(file.read())
            encoding = result['encoding']

        self.update_cache(path, encoding)
        return encoding

    def get_encoding(self, path: Path) -> str:
        if path in self.encoding_cache:
            return self.encoding_cache[path]
        else:
            return self.detect_encoding(path)

    def update_cache(self, path: Path, encoding: str) -> None:
        self.encoding_cache[path] = encoding

        if self.max_cache_size is not None and len(self.encoding_cache) > self.max_cache_size:
            self.encoding_cache.popitem(last=False)