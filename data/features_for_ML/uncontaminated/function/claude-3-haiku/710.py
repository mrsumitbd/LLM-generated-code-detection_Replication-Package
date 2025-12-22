import random
from typing import Any, Dict

def generate_example(rng: random.Random, difficulty: float = 1.0) -> Dict[str, Any]:
    example = {
        "number": rng.uniform(0, 10 * difficulty),
        "text": "".join(rng.choices("abcdefghijklmnopqrstuvwxyz", k=int(10 * difficulty))),
        "boolean": rng.choice([True, False]),
        "list": rng.sample(range(int(20 * difficulty)), k=int(5 * difficulty))
    }
    return example