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
        selectedItems (list[str]): A dictionary mapping directory paths to the
            list of selected items in that directory.
        search (str): The current search string.
    """

    def __init__(self) -> None:
        self.directories = []
        self.historyIndex = -1
        self.lastHighlighted = {}
        self.selectMode = False
        self.selectedItems = {}
        self.search = ""

    def add_directory(self, directory: dict) -> None:
        """Add a new directory to the session history."""
        self.directories.insert(0, directory)
        self.historyIndex = 0

    def remove_directory(self, index: int) -> None:
        """Remove a directory from the session history."""
        if index < 0 or index >= len(self.directories):
            return
        del self.directories[index]
        if self.historyIndex >= index:
            self.historyIndex -= 1

    def set_last_highlighted(self, directory: str, index: int) -> None:
        """Set the last highlighted item index for a directory."""
        self.lastHighlighted[directory] = index

    def get_last_highlighted(self, directory: str) -> int:
        """Get the last highlighted item index for a directory."""
        return self.lastHighlighted.get(directory, 0)

    def toggle_select_mode(self) -> None:
        """Toggle the select mode."""
        self.selectMode = not self.selectMode

    def add_selected_item(self, directory: str, item: str) -> None:
        """Add an item to the selected items list for a directory."""
        if directory not in self.selectedItems:
            self.selectedItems[directory] = []
        self.selectedItems[directory].append(item)

    def remove_selected_item(self, directory: str, item: str) -> None:
        """Remove an item from the selected items list for a directory."""
        if directory in self.selectedItems:
            self.selectedItems[directory].remove(item)

    def clear_selected_items(self, directory: str) -> None:
        """Clear the selected items list for a directory."""
        if directory in self.selectedItems:
            self.selectedItems[directory].clear()

    def set_search(self, search: str) -> None:
        """Set the current search string."""
        self.search = search