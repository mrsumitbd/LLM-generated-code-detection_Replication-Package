from typing import List, Tuple

class State:

    def __init__(self, items: List[Tuple[int, int]], k: int) -> None:
        self.items = items
        self.k = k

    def spread(self):
        pass

    def get_partitions(self):
        pass

    def merge(self, other):
        pass

    @property
    def spread(self) -> int:
        pass

    def __lt__(self, other):
        pass

    def __repr__(self) -> str:
        pass