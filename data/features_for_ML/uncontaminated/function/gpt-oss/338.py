from random import Random
from typing import Any, Dict

def generate_example(rng: Random, difficulty: float = 1.0) -> Dict[str, Any]:
    """
    Generate a simple example dictionary based on the provided random number generator
    and difficulty level.

    Parameters
    ----------
    rng : Random
        A random number generator instance.
    difficulty : float, optional
        A multiplier that influences the size of the generated data. Defaults to 1.0.

    Returns
    -------
    dict[str, Any]
        A dictionary containing:
            - "values": a list of random integers.
            - "sum": the sum of those integers.
            - "difficulty": the difficulty level used.
    """
    # Ensure at least one element
    count = max(1, int(difficulty * 10))
    values = [rng.randint(0, 100) for _ in range(count)]
    return {
        "values": values,
        "sum": sum(values),
        "difficulty": difficulty,
    }