class LRUCache:
    class _Node:
        __slots__ = ("key", "value", "prev", "next")
        def __init__(self, key=None, value=None):
            self.key = key
            self.value = value
            self.prev = None
            self.next = None

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.cache = {}
        # Dummy head and tail to avoid edge checks
        self.head = self._Node()
        self.tail = self._Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: "_Node") -> None:
        prev, nxt = node.prev, node.next
        prev.next = nxt
        nxt.prev = prev

    def _add_to_front(self, node: "_Node") -> None:
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._add_to_front(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._remove(node)
            self._add_to_front(node)
        else:
            if len(self.cache) >= self.capacity:
                # Remove LRU node
                lru = self.tail.prev
                self._remove(lru)
                del self.cache[lru.key]
            new_node = self._Node(key, value)
            self.cache[key] = new_node
            self._add_to_front(new_node)