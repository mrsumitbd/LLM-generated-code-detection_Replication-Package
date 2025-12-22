import os
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

class Book:

    def __init__(self, book_dir: str, file_path: str):
        self.book_dir = book_dir
        self.file_path = file_path
        self.metadata = self._load_metadata()

    def _load_metadata(self) -> dict:
        """Load metadata from metadata.opf file if it exists."""
        metadata_path = os.path.join(self.book_dir, 'metadata.opf')
        if os.path.exists(metadata_path):
            try:
                import xml.etree.ElementTree as ET
                tree = ET.parse(metadata_path)
                root = tree.getroot()
                return self._parse_opf(root)
            except Exception:
                return {}
        return {}

    def _parse_opf(self, root) -> dict:
        """Parse OPF XML metadata."""
        metadata = {}
        ns = {
            'opf': 'http://www.idpf.org/2007/opf',
            'dc': 'http://purl.org/dc/elements/1.1/'
        }
        
        try:
            title_elem = root.find('.//dc:title', ns)
            if title_elem is not None:
                metadata['title'] = title_elem.text
            
            author_elem = root.find('.//dc:creator', ns)
            if author_elem is not None:
                metadata['author'] = author_elem.text
            
            date_elem = root.find('.//dc:date', ns)
            if date_elem is not None:
                metadata['date'] = date_elem.text
        except Exception:
            pass
        
        return metadata

    def get_split_library(self) -> dict[str, str] | None:
        """Extract library information from file path."""
        parts = self.file_path.split(os.sep)
        if len(parts) >= 2:
            return {
                'library': parts[0],
                'path': os.sep.join(parts[1:])
            }
        return None

    def get_calibre_library(self) -> str:
        """Get the calibre library name from the book directory."""
        return os.path.basename(os.path.dirname(self.book_dir))

    def get_time(self) -> str:
        """Get the modification time of the book file."""
        if os.path.exists(self.file_path):
            timestamp = os.path.getmtime(self.file_path)
            return datetime.fromtimestamp(timestamp).isoformat()
        return datetime.now().isoformat()

    def get_title_and_author(self) -> tuple[str, str, str]:
        """Get title, author, and file name."""
        title = self.metadata.get('title', 'Unknown')
        author = self.metadata.get('author', 'Unknown')
        file_name = os.path.basename(self.file_path)
        return (title, author, file_name)

    def get_new_metadata_path(self) -> str:
        """Generate a new metadata file path."""
        base_name = os.path.splitext(os.path.basename(self.file_path))[0]
        return os.path.join(self.book_dir, f"{base_name}_metadata.json")

    def export_as_dict(self) -> dict[str, str | None]:
        """Export book information as a dictionary."""
        title, author, file_name = self.get_title_and_author()
        split_lib = self.get_split_library()
        
        return {
            'title': title,
            'author': author,
            'file_name': file_name,
            'file_path': self.file_path,
            'book_dir': self.book_dir,
            'calibre_library': self.get_calibre_library(),
            'time': self.get_time(),
            'library': split_lib.get('library') if split_lib else None,
            'metadata_path': self.get_new_metadata_path()
        }