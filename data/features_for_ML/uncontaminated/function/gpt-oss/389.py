import typing as T
import itertools

def get_llm_name_combinations(
    llm_names: T.List[str],
    n_llms: T.List[int],
    with_replacement=True,
) -> T.List[str]:
    """
    Generate all possible combinations of LLM names for the given list of
    desired combination sizes.

    Parameters
    ----------
    llm_names : List[str]
        The list of available LLM names.
    n_llms : List[int]
        A list of integers specifying the desired combination sizes.
    with_replacement : bool, default=True
        If True, the same LLM name may appear multiple times in a combination.
        If False, each LLM name can appear at most once in a combination.

    Returns
    -------
    List[str]
        A list of comma‑separated strings, each representing one combination.
    """
    if not llm_names:
        return []

    result: T.List[str] = []

    for size in n_llms:
        if size <= 0:
            continue

        if with_replacement:
            # Use product to allow repeated names
            for combo in itertools.product(llm_names, repeat=size):
                result.append(",".join(combo))
        else:
            # Use combinations to avoid repeats
            for combo in itertools.combinations(llm_names, size):
                result.append(",".join(combo))

    return result