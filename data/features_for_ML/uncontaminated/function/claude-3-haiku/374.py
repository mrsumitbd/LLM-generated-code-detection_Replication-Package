from typing import List, Tuple

class CayleyGraphDef:
    def __init__(self, generators: List[Tuple[int, int]]):
        self.generators = generators

def signed_reversals(n: int) -> CayleyGraphDef:
    generators = []
    for i in range(1, n+1):
        generators.append((i, n+i))
    return CayleyGraphDef(generators)