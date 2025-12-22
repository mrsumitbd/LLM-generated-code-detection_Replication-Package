import typing as T
from itertools import product

def get_llm_name_combinations(
    llm_names: T.List[str],
    n_llms: T.List[int],
    with_replacement=True,
) -> T.List[str]:
    if with_replacement:
        return [''.join(combo) for combo in product(llm_names, repeat=sum(n_llms))]
    else:
        return [''.join(combo) for combo in product(*(llm_names[:n] for n in n_llms))]