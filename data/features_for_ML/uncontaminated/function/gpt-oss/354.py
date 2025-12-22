from random import Random
from typing import Any, Dict

def generate_example(rng: Random, difficulty: float = 1.0) -> Dict[str, Any]:
    """
    Generate a simple example dictionary based on the provided difficulty level.
    The dictionary contains:
        - 'values': a list of random floats whose length scales with difficulty.
        - 'difficulty': the difficulty value used to generate the example.
    """
    # Clamp difficulty to a reasonable range to avoid extreme sizes
    difficulty = max(0.0, min(difficulty, 10.0))

    # Determine the number of random values to generate
    # Scale the count linearly with difficulty, ensuring at least one value
    count = max(1, int(round(5 * difficulty)))

    # Generate the random values
    values = [rng.random() for _ in range(count)]

    return {
        "values": values,
        "difficulty": difficulty,
    }