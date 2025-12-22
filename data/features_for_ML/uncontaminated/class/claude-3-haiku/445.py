from typing import Iterable, Tuple, List
from itertools import combinations

Element = str

class CNF:
    def __init__(self, clauses: List[Tuple[Element, ...]]):
        self.clauses = clauses

    def __repr__(self) -> str:
        return str(self.clauses)

class Q:
    """Quantifier for the number of elements that are true

    >>> Q(['A', 'B', 'C']) <= 1
    [('~A', '~B'),
    ('~A', '~C'),
    ('~B', '~C')]
    """

    def __init__(self, elements: Iterable[Element]):
        self.elements = list(elements)

    def __lt__(self, n: int) -> CNF:
        clauses = [tuple('~' + e for e in c) for c in combinations(self.elements, len(self.elements) - n)]
        return CNF(clauses)

    def __le__(self, n: int) -> CNF:
        clauses = [tuple('~' + e for e in c) for c in combinations(self.elements, len(self.elements) - n + 1)]
        return CNF(clauses)

    def __gt__(self, n: int) -> CNF:
        clauses = [tuple('~' + e for e in c) for c in combinations(self.elements, n + 1)]
        return CNF(clauses)

    def __ge__(self, n: int) -> CNF:
        clauses = [tuple('~' + e for e in c) for c in combinations(self.elements, n)]
        return CNF(clauses)

    def __eq__(self, n: int) -> CNF:
        clauses = [tuple('~' + e for e in c) for c in combinations(self.elements, len(self.elements) - n)] + \
                  [tuple('~' + e for e in c) for c in combinations(self.elements, n)]
        return CNF(clauses)

    def __ne__(self, n: int) -> CNF:
        clauses = [tuple('~' + e for e in c) for c in combinations(self.elements, len(self.elements) - n + 1)] + \
                  [tuple('~' + e for e in c) for c in combinations(self.elements, n + 1)]
        return CNF(clauses)

    def __repr__(self) -> str:
        return f"Q({self.elements})"