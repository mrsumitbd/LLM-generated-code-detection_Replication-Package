from itertools import combinations
from typing import FrozenSet, Iterable

class Q:
    """Quantifier for the number of elements that are true

    >>> Q(['A', 'B', 'C']) <= 1
    [('~A', '~B'),
    ('~A', '~C'),
    ('~B', '~C')]
    """

    def __init__(self, elements: Iterable[Element]):
        self.elements = tuple(elements)

    def __lt__(self, n: int) -> CNF:
        return list(combinations(map(neg, self.elements), n))

    def __le__(self, n: int) -> CNF:
        return self < n + 1

    def __gt__(self, n: int) -> CNF:
        return list(combinations(self.elements, len(self.elements) - n))

    def __ge__(self, n: int) -> CNF:
        return self > n - 1

    def __eq__(self, n: int) -> CNF:  # type:ignore
        return (self <= n) + (self >= n)

    def __ne__(self, n) -> CNF:  # type:ignore
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(elements={self.elements!r})"