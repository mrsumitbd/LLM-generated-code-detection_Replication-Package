from pathlib import Path
from typing import Optional, Dict
import chardet
from functools import lru_cache


class EncodingManager:
    """Manages file encodings across multiple operations to ensure consistency."""

    def __init__(self, max_cache_size: Optional[int] = None):
        self._cache: Dict[str, str] = {}
        self._max_cache_size = max_cache_size or 128
        self._access_order: list = []

    def detect_encoding(self, path: Path) -> str:
        """Detect the encoding of a file by reading a sample of its content."""
        path = Path(path)
        
        try:
            with open(path, 'rb') as f:
                raw_data = f.read(10000)
            
            if not raw_data:
                return 'utf-8'
            
            detected = chardet.detect(raw_data)
            encoding = detected.get('encoding', 'utf-8')
            
            if encoding is None:
                encoding = 'utf-8'
            
            return encoding.lower()
        except (IOError, OSError):
            return 'utf-8'

    def get_encoding(self, path: Path) -> str:
        """Get the encoding for a file, using cache if available."""
        path = Path(path)
        path_str = str(path.resolve())
        
        if path_str in self._cache:
            self._access_order.remove(path_str)
            self._access_order.append(path_str)
            return self._cache[path_str]
        
        encoding = self.detect_encoding(path)
        
        if len(self._cache) >= self._max_cache_size:
            oldest = self._access_order.pop(0)
            del self._cache[oldest]
        
        self._cache[path_str] = encoding
        self._access_order.append(path_str)
        
        return encoding