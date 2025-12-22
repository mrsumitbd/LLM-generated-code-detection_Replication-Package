from itertools import combinations, combinations_with_replacement
import typing as T

def get_llm_name_combinations(
    llm_names: T.List[str],
    n_llms: T.List[int],
    with_replacement=True,
) -> T.List[str]:
    generator = (
        (lambda elements, n: list(combinations_with_replacement(elements, n)))
        if with_replacement
        else (lambda elements, n: list(combinations(elements, n)))
    )
    llm_combinations = []
    for n in n_llms:
        if n <= len(llm_names):
            llm_combinations_n = [str(c) for c in generator(llm_names, n)]
            llm_combinations.extend(llm_combinations_n)
    return llm_combinations