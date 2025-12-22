from random import Random
from typing import Any

def generate_example(rng: Random, difficulty: float = 1.0) -> dict[str, Any]:
    example = {
        "name": rng.choice(["Alice", "Bob", "Charlie"]),
        "age": rng.randint(18, 60),
        "score": rng.uniform(0.0, 100.0) * difficulty
    }
    return example