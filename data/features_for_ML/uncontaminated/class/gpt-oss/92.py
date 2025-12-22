from __future__ import annotations
from typing import List, Tuple, Iterable
import itertools


class State:
    def __init__(self, items: List[Tuple[int, int]], k: int) -> None:
        """
        Initialize a state with a list of items and a target number of partitions k.
        Items are stored sorted by their first element to make partition generation
        deterministic.
        """
        self.items: List[Tuple[int, int]] = sorted(items, key=lambda x: x[0])
        self.k: int = k
        self._spread: int | None = None

    def spread(self) -> int:
        """
        Compute the spread of the current state.
        The spread is defined as the difference between the maximum and minimum
        first elements of the items.
        """
        if not self.items:
            return 0
        values = [x[0] for x in self.items]
        self._spread = max(values) - min(values)
        return self._spread

    @property
    def spread(self) -> int:
        """
        Property to access the cached spread value. If it hasn't been computed
        yet, compute it first.
        """
        if self._spread is None:
            self.spread()
        return self._spread

    def get_partitions(self) -> List[List[List[Tuple[int, int]]]]:
        """
        Generate all possible ways to partition the items into exactly k groups.
        Each partition is represented as a list of k lists of items.
        The groups are ordered by the smallest index of the first element in
        each group to avoid duplicate permutations.
        """
        def _partitions(remaining: List[Tuple[int, int]], groups_left: int) -> Iterable[List[List[Tuple[int, int]]]]:
            if groups_left == 1:
                yield [remaining]
                return
            n = len(remaining)
            # choose a non-empty subset for the first group
            # to avoid duplicates, enforce that the first element of the first group
            # has the smallest index among all groups
            for r in range(1, n - groups_left + 2):  # at least 1, at most n - groups_left + 1
                for combo in itertools.combinations(range(n), r):
                    first_group = [remaining[i] for i in combo]
                    # ensure ordering: the smallest index in first_group must be the smallest
                    # among all groups (this is automatically satisfied by the recursion order)
                    rest = [remaining[i] for i in range(n) if i not in combo]
                    for rest_part in _partitions(rest, groups_left - 1):
                        yield [first_group] + rest_part

        return list(_partitions(self.items, self.k))

    def merge(self, other: State) -> State:
        """
        Merge this state with another state by concatenating their items.
        The resulting state keeps the same k value as the original states.
        """
        if self.k != other.k:
            raise ValueError("Cannot merge states with different k values")
        merged_items = self.items + other.items
        return State(merged_items, self.k)

    def __lt__(self, other: State) -> bool:
        """
        Compare two states based on their spread. A state with a smaller spread
        is considered less than a state with a larger spread.
        """
        if not isinstance(other, State):
            return NotImplemented
        return self.spread < other.spread

    def __repr__(self) -> str:
        return f"State(items={self.items}, k={self.k}, spread={self.spread})"