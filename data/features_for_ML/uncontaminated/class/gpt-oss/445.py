from __future__ import annotations
from typing import Iterable, List, Tuple, Any
import itertools

# Type alias for CNF: a list of clauses, each clause is a tuple of literals (strings)
CNF = List[Tuple[str, ...]]
Element = Any  # In this implementation we treat elements as strings

class Q:
    """Quantifier for the number of elements that are true

    >>> Q(['A', 'B', 'C']) <= 1
    [('~A', '~B'), ('~A', '~C'), ('~B', '~C')]
    """

    def __init__(self, elements: Iterable[Element]):
        self.elements = list(elements)

    def _neg(self, e: Element) -> str:
        """Return the negated literal for an element."""
        return f"~{e}"

    def _at_most(self, n: int) -> CNF:
        """Generate CNF clauses for at most n true elements."""
        if n < 0:
            # No assignment satisfies at most negative number of trues
            return []
        if n >= len(self.elements):
            # Always satisfied
            return []
        clauses: CNF = []
        for combo in itertools.combinations(self.elements, n + 1):
            clause = tuple(self._neg(e) for e in combo)
            clauses.append(clause)
        return clauses

    def _at_least(self, n: int) -> CNF:
        """Generate CNF clauses for at least n true elements."""
        if n <= 0:
            # Always satisfied
            return []
        if n > len(self.elements):
            # Impossible
            return []
        # At least n true is equivalent to at most len-n false
        return self._at_most(len(self.elements) - n)

    def __lt__(self, n: int) -> CNF:
        return self._at_most(n - 1)

    def __le__(self, n: int) -> CNF:
        return self._at_most(n)

    def __gt__(self, n: int) -> CNF:
        return self._at_least(n + 1)

    def __ge__(self, n: int) -> CNF:
        return self._at_least(n)

    def __eq__(self, n: int) -> CNF:  # type:ignore
        return self._at_most(n) + self._at_least(n)

    def __ne__(self, n) -> CNF:  # type:ignore
        # Not equal: either at most n-1 or at least n+1
        # CNF cannot express disjunction directly; we return the conjunction of both
        return self._at_most(n - 1) + self._at_least(n + 1)

    def __repr__(self) -> str:
        return f"Q({self.elements!r})"