class MessageCache:

    def __init__(self, max_size: int = 10000):
        self.max_size = max_size
        self.cache = {}
        self.access_order = []

    def get_message(self, id: str) -> "Message | None":
        if id in self.cache:
            self.access_order.remove(id)
            self.access_order.append(id)
            return self.cache[id]
        return None

    def add_message(self, message: Message):
        if message.id in self.cache:
            self.access_order.remove(message.id)
        elif len(self.cache) >= self.max_size:
            lru_id = self.access_order.pop(0)
            del self.cache[lru_id]
        
        self.cache[message.id] = message
        self.access_order.append(message.id)