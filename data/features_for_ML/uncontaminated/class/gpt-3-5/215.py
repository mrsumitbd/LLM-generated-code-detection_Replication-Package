from typing import Any

class ResearchAgent:

    def __init__(self, app: Any, thread: MessageThread):
        self.app = app
        self.thread = thread