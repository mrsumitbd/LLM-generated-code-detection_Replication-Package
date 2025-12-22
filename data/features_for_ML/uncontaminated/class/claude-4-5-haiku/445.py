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
        return self.__le__(n - 1)

    def __le__(self, n: int) -> CNF:
        if n < 0:
            return [()]
        if n >= len(self.elements):
            return []
        
        clauses = []
        for combo in combinations(self.elements, n + 1):
            clause = tuple(f'~{elem}' for elem in combo)
            clauses.append(clause)
        return clauses

    def __gt__(self, n: int) -> CNF:
        return self.__ge__(n + 1)

    def __ge__(self, n: int) -> CNF:
        if n <= 0:
            return []
        if n > len(self.elements):
            return [()]
        
        clauses = []
        for combo in combinations(self.elements, len(self.elements) - n + 1):
            clause = tuple(str(elem) for elem in combo)
            clauses.append(clause)
        return clauses

    def __eq__(self, n: int) -> CNF:
        if n < 0 or n > len(self.elements):
            return [()]
        
        le_clauses = self.__le__(n)
        ge_clauses = self.__ge__(n)
        return le_clauses + ge_clauses

    def __ne__(self, n) -> CNF:
        if n < 0 or n > len(self.elements):
            return []
        
        lt_clauses = self.__lt__(n)
        gt_clauses = self.__gt__(n)
        return lt_clauses + gt_clauses

    def __repr__(self) -> str:
        return f"Q({self.elements!r})"