import time

class QuestionMaker:

    def __init__(self, chat_id: str, context: str = "") -> None:
        self.chat_id = chat_id
        self.context = context

    def get_context(self, timestamp: float = time.time()) -> str:
        return f"Chat ID: {self.chat_id}, Context: {self.context}, Timestamp: {timestamp}"