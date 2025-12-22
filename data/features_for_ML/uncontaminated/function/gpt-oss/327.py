import random
from typing import Any, Iterable, List, Tuple, Union

def _select_choice(choices: Iterable[Any], rls_data: dict) -> Any:
    """
    Select a choice from `choices` based on optional weighting or explicit index.

    Parameters
    ----------
    choices : Iterable
        A sequence of choices. Each element may be:
          * a plain value (no weighting)
          * a tuple/list of the form (value, weight) where weight is a
            non‑negative number.
    rls_data : dict
        Optional data controlling selection:
          * 'choice' : int index to select directly (if valid).
          * 'random' : a random.Random instance to use.
          * 'seed'   : a seed value to initialise a new Random instance.

    Returns
    -------
    Any
        The selected choice, or None if `choices` is empty.
    """
    # Convert to list for repeated indexing
    choices_list = list(choices)
    if not choices_list:
        return None

    # If an explicit index is provided and valid, use it
    idx = rls_data.get("choice")
    if isinstance(idx, int) and 0 <= idx < len(choices_list):
        return choices_list[idx]

    # Determine the random generator to use
    rng = rls_data.get("random")
    if rng is None:
        seed = rls_data.get("seed")
        rng = random.Random(seed)

    # Check if choices are weighted
    weighted = False
    weights: List[Union[int, float]] = []
    for item in choices_list:
        if isinstance(item, (tuple, list)) and len(item) == 2:
            _, w = item
            if isinstance(w, (int, float)) and w >= 0:
                weighted = True
                weights.append(w)
            else:
                weighted = False
                break
        else:
            weighted = False
            break

    if weighted:
        total = sum(weights)
        if total == 0:
            # All weights zero – fall back to uniform random choice
            return rng.choice(choices_list)
        r = rng.uniform(0, total)
        cumulative = 0.0
        for (value, weight) in choices_list:
            cumulative += weight
            if r <= cumulative:
                return value
        # Fallback: return last value
        return choices_list[-1][0]
    else:
        # Uniform random choice
        return rng.choice(choices_list)