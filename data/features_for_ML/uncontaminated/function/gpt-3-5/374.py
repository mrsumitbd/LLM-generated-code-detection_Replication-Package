from sympy.combinatorics.generators import CayleyGraphDef

def signed_reversals(n: int) -> CayleyGraphDef:
    def signed_reverse(s):
        return s[::-1].swapcase()

    elements = [str(i) for i in range(1, n+1)] + [str(i) for i in range(1, n+1)]
    generators = []
    for i in range(1, n+1):
        for j in range(i, n+1):
            generators.append(f'R[{i}..{j}]')

    relations = []
    for i in range(1, n+1):
        for j in range(i, n+1):
            relations.append((f'R[{i}..{j}]', signed_reverse(f'R[{i}..{j}]')))

    return CayleyGraphDef(elements, generators, relations)