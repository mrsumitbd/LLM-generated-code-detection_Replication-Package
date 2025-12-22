class State:
    def __init__(self, items: List[Tuple[int, int]], k: int) -> None:
        self.items = items
        self.k = k
        self.partitions = self.get_partitions()
        self.spread_value = self.spread

    def spread(self) -> int:
        if not self.partitions:
            return 0
        return max(partition[-1] - partition[0] for partition in self.partitions)

    def get_partitions(self) -> List[List[int]]:
        if not self.items:
            return []

        self.items.sort(key=lambda x: x[0])
        partitions = []
        current_partition = [self.items[0][0], self.items[0][1]]

        for item in self.items[1:]:
            if item[0] <= current_partition[-1]:
                current_partition[1] = max(current_partition[1], item[1])
            else:
                partitions.append(current_partition)
                current_partition = [item[0], item[1]]

        partitions.append(current_partition)
        return partitions

    def merge(self, other: 'State') -> 'State':
        merged_items = self.items + other.items
        return State(merged_items, self.k + other.k)

    def __lt__(self, other: 'State') -> bool:
        return self.spread < other.spread or (self.spread == other.spread and self.k < other.k)

    def __repr__(self) -> str:
        return f"State(items={self.items}, k={self.k}, spread={self.spread})"