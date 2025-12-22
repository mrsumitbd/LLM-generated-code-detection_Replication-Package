def get_llm_name_combinations(llm_names, n_llms, with_replacement=True):
    from itertools import product, combinations_with_replacement
    
    if with_replacement:
        combinations = product(llm_names, repeat=sum(n_llms))
    else:
        combinations = product(llm_names, repeat=len(n_llms))
    
    return [''.join(comb) for comb in combinations]