class State:
    def __init__(self, items: List[Tuple[int, int]], k: int) -> None:
        self.items = sorted(items)
        self.k = k
        self._spread = self._calculate_spread()

    def _calculate_spread(self) -> int:
        if not self.items:
            return 0
        return self.items[-1][0] - self.items[0][0]

    def spread(self):
        """Method version of spread calculation"""
        return self._spread

    def get_partitions(self):
        """Partition items into k groups"""
        if not self.items or self.k <= 0:
            return []
        
        if self.k >= len(self.items):
            return [[item] for item in self.items]
        
        partitions = [[] for _ in range(self.k)]
        for i, item in enumerate(self.items):
            partitions[i % self.k].append(item)
        
        return partitions

    def merge(self, other):
        """Merge two states"""
        if not isinstance(other, State):
            return None
        
        merged_items = list(set(self.items + other.items))
        merged_k = max(self.k, other.k)
        return State(merged_items, merged_k)

    @property
    def spread(self) -> int:
        """Property to get spread value"""
        return self._spread

    def __lt__(self, other):
        """Less than comparison based on spread"""
        if not isinstance(other, State):
            return NotImplemented
        return self._spread < other._spread

    def __repr__(self) -> str:
        return f"State(items={self.items}, k={self.k}, spread={self._spread})"