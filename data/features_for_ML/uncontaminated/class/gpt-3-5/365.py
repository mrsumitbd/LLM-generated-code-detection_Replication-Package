class SessionManager:
    def __init__(self) -> None:
        self.directories = []
        self.historyIndex = 0
        self.lastHighlighted = {}
        self.selectMode = False
        self.selectedItems = {}
        self.search = ""