class Message:
    def __init__(self, id: str, content: str):
        self.id = id
        self.content = content

class MessageCache:
    def __init__(self, max_size: int = 10000):
        self.max_size = max_size
        self.cache = {}
        self.lru_queue = []

    def get_message(self, id: str) -> "Message | None":
        if id in self.cache:
            self.lru_queue.remove(id)
            self.lru_queue.append(id)
            return self.cache[id]
        return None

    def add_message(self, message: Message):
        if len(self.cache) == self.max_size:
            evict_id = self.lru_queue.pop(0)
            del self.cache[evict_id]
        self.cache[message.id] = message
        self.lru_queue.append(message.id)