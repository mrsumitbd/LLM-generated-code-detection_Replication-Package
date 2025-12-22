from __future__ import annotations
from typing import Dict, List, Optional


class SessionManager:
    """Manages session-related variables.

    Attributes:
        directories (list[dict]): A list of dictionaries that contain a
            directory's name within. The closer it is to index 0, the
            older it is.
        historyIndex (int): The index of the session in the directories.
            This can be a number between 0 and the length of the list - 1,
            inclusive.
        lastHighlighted (dict[str, int]): A dictionary mapping directory paths
            to the index of the last highlighted item. If a directory is not
            in the dictionary, the default is 0.
        selectMode (bool): Whether select mode is enabled for that directory.
        selectedItems (dict[str, list[str]]): A dictionary mapping directory
            paths to the list of selected items in that directory.
        search (str): The current search string.
    """

    def __init__(self) -> None:
        self.directories: List[Dict] = []
        self.historyIndex: int = -1
        self.lastHighlighted: Dict[str, int] = {}
        self.selectMode: bool = False
        self.selectedItems: Dict[str, List[str]] = {}
        self.search: str = ""

    # ------------------------------------------------------------------
    # Directory / history handling
    # ------------------------------------------------------------------
    def add_directory(self, directory: Dict) -> None:
        """Add a new directory to the history and set it as current."""
        self.directories.append(directory)
        self.historyIndex = len(self.directories) - 1

    def get_current_directory(self) -> Optional[Dict]:
        """Return the current directory dict or None if history is empty."""
        if 0 <= self.historyIndex < len(self.directories):
            return self.directories[self.historyIndex]
        return None

    def move_history(self, delta: int) -> None:
        """Move the history index by delta, clamped to valid range."""
        if not self.directories:
            return
        new_index = self.historyIndex + delta
        self.historyIndex = max(0, min(new_index, len(self.directories) - 1))

    # ------------------------------------------------------------------
    # Highlight handling
    # ------------------------------------------------------------------
    def set_last_highlighted(self, path: str, index: int) -> None:
        """Set the last highlighted index for a given directory path."""
        self.lastHighlighted[path] = index

    def get_last_highlighted(self, path: str) -> int:
        """Get the last highlighted index for a given directory path."""
        return self.lastHighlighted.get(path, 0)

    # ------------------------------------------------------------------
    # Select mode handling
    # ------------------------------------------------------------------
    def toggle_select_mode(self) -> None:
        """Toggle the select mode flag."""
        self.selectMode = not self.selectMode

    # ------------------------------------------------------------------
    # Selected items handling
    # ------------------------------------------------------------------
    def add_selected_item(self, path: str, item: str) -> None:
        """Add an item to the selected list for a directory."""
        self.selectedItems.setdefault(path, []).append(item)

    def remove_selected_item(self, path: str, item: str) -> None:
        """Remove an item from the selected list for a directory."""
        items = self.selectedItems.get(path)
        if items and item in items:
            items.remove(item)
            if not items:
                del self.selectedItems[path]

    def clear_selected_items(self, path: str) -> None:
        """Clear all selected items for a directory."""
        self.selectedItems.pop(path, None)

    # ------------------------------------------------------------------
    # Search handling
    # ------------------------------------------------------------------
    def set_search(self, query: str) -> None:
        """Set the current search string."""
        self.search = query

    def clear_search(self) -> None:
        """Clear the current search string."""
        self.search = ""