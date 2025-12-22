import time

class QuestionMaker:
    def __init__(self, chat_id: str, context: str = "") -> None:
        self.chat_id = chat_id
        self.context = context
        self.timestamp = time.time()

    def get_context(self, timestamp: float = time.time()) -> str:
        if timestamp != self.timestamp:
            self.timestamp = timestamp
            return self.context
        else:
            return self.context