from itertools import combinations
from typing import Iterable, List

class Q:
    """Quantifier for the number of elements that are true

    >>> Q(['A', 'B', 'C']) <= 1
    [('~A', '~B'),
    ('~A', '~C'),
    ('~B', '~C')]
    """

    def __init__(self, elements: Iterable[str]):
        self.elements = list(elements)

    def __lt__(self, n: int) -> List[List[str]]:
        return self._generate_cnf(n, '<')

    def __le__(self, n: int) -> List[List[str]]:
        return self._generate_cnf(n, '<=')

    def __gt__(self, n: int) -> List[List[str]]:
        return self._generate_cnf(n, '>')

    def __ge__(self, n: int) -> List[List[str]]:
        return self._generate_cnf(n, '>=')

    def __eq__(self, n: int) -> List[List[str]]:
        return self._generate_cnf(n, '==')

    def __ne__(self, n: int) -> List[List[str]]:
        return self._generate_cnf(n, '!=')

    def __repr__(self) -> str:
        return f"Q({self.elements})"

    def _generate_cnf(self, n: int, op: str) -> List[List[str]]:
        cnf = []
        for combo in combinations(self.elements, n+1 if op in ('<', '<=') else n):
            clause = []
            for element in self.elements:
                if element in combo:
                    clause.append(element)
                else:
                    clause.append(f"~{element}")
            cnf.append(clause)
        return cnf