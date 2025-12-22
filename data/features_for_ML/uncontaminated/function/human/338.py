from typing import Any
from random import Random

def generate_example(rng: Random, difficulty: float = 1.0) -> dict[str, Any]:
        names = ["Sam", "Harry", "Tom", "John", "Mike", "Dave", "Steve", "Bob"]
        units = ["feet", "yards", "meters"]

        name1, name2 = rng.sample(names, 2)
        unit = rng.choice(units)

        # Start with the difference - must be divisible by 10 and between 20 and 180
        max_diff = min(int(200 * difficulty), 180)
        diff = 10 * rng.randint(2, max_diff // 10)  # This ensures diff is multiple of 10 between 20 and max_diff

        # For total: we need total > diff + 20 and (total - diff) must be even
        # Let's work backwards from our constraints
        min_total = diff + 22  # Adding 22 ensures total-diff > 10 and gives room for even adjustment
        max_total = min(int(1000 * difficulty), min_total + 200)  # Cap the maximum to avoid too large numbers

        # Ensure max_total is larger than min_total and generate valid number
        if max_total <= min_total:
            total = min_total
        else:
            # Generate total as min_total plus an even number
            total = min_total + (2 * rng.randint(0, (max_total - min_total) // 2))

        result = generate_from_variables(name1, name2, total, diff, unit)

        return {
            "question": result["question"],
            "answer": result["answer"],
            "metadata": {
                "difficulty": difficulty,
                "answer_value": result["answer_value"],
                "answer_cot": result["answer_cot"],
                "variables": result["variables"],
            },
        }