from __future__ import annotations

import string
from random import Random
from typing import Any, Dict

def generate_example(rng: Random, difficulty: float = 1.0) -> Dict[str, Any]:
    """
    Generate a deterministic example dictionary based on a random number generator
    and a difficulty level.

    Parameters
    ----------
    rng : Random
        A random number generator instance.
    difficulty : float, optional
        A multiplier that controls the size and complexity of the generated data.
        The default is 1.0.

    Returns
    -------
    dict[str, Any]
        A dictionary containing:
        - ``numbers``: a list of random integers.
        - ``text``: a random string.
        - ``nested``: a dictionary with random float values.
    """
    # Ensure difficulty is positive and not too large
    difficulty = max(0.1, min(difficulty, 10.0))

    # Number of items to generate
    n_items = max(1, int(difficulty * 5))

    # Random integers between 0 and 100
    numbers = [rng.randint(0, 100) for _ in range(n_items)]

    # Random string of length 8
    text_length = 8
    text = ''.join(rng.choice(string.ascii_lowercase) for _ in range(text_length))

    # Nested dictionary with random float values
    nested = {f"key_{i}": rng.random() for i in range(n_items)}

    return {
        "numbers": numbers,
        "text": text,
        "nested": nested,
    }