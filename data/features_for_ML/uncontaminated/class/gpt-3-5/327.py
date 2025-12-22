class MessageCache:
    
    def __init__(self, max_size: int = 10000):
        self.max_size = max_size
        self.cache = {}

    def get_message(self, id: str) -> "Message | None":
        return self.cache.get(id, None)

    def add_message(self, message: Message):
        if len(self.cache) >= self.max_size:
            oldest_message_id = next(iter(self.cache))
            del self.cache[oldest_message_id]
        self.cache[message.id] = message