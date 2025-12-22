import typing as T
from itertools import combinations_with_replacement, combinations

def get_llm_name_combinations(
    llm_names: T.List[str],
    n_llms: T.List[int],
    with_replacement=True,
) -> T.List[str]:
    result = []
    
    for n in n_llms:
        if with_replacement:
            combos = combinations_with_replacement(llm_names, n)
        else:
            combos = combinations(llm_names, n)
        
        for combo in combos:
            result.append(",".join(combo))
    
    return result