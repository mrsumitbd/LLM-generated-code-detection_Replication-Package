from __future__ import annotations

import time
from random import Random
from typing import Any, Dict

def generate_example(rng: Random, difficulty: float = 1.0) -> Dict[str, Any]:
    """
    Generate a simple example dictionary that contains a small arithmetic problem.
    The difficulty parameter controls the size of the numbers used in the problem.
    """
    # Determine the range of numbers based on difficulty
    if difficulty < 1.0:
        max_val = 10
    elif difficulty < 2.0:
        max_val = 100
    else:
        max_val = 1000

    # Randomly choose an operation
    op = rng.choice(["+", "*"])

    # Generate operands
    a = rng.randint(1, max_val)
    b = rng.randint(1, max_val)

    # Compute the answer
    if op == "+":
        answer = a + b
    else:
        answer = a * b

    # Build the example dictionary
    example: Dict[str, Any] = {
        "id": rng.randint(1, 10_000),
        "question": f"{a} {op} {b}",
        "answer": answer,
        "difficulty": difficulty,
        "generated_at": time.time(),
    }

    return example