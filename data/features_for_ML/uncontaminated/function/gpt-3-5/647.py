from sympy.combinatorics import Permutation
from sympy.combinatorics.generators import transpositions, cyclic_shifts
from sympy.combinatorics.named_groups import SymmetricGroup

def larx(n: int) -> CayleyGraphDef:
    S_n = SymmetricGroup(n)
    generators = [Permutation(t) for t in transpositions(n)] + [Permutation(c) for c in cyclic_shifts(n)]
    return CayleyGraph(S_n, generators)