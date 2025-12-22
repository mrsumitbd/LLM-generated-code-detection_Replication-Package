from random import Random
from typing import Any

def generate_example(rng: Random, difficulty: float = 1.0) -> dict[str, Any]:
        names = ["Mrs. Smith", "Ms. Johnson", "Dr. Patel", "Mrs. Lee"]
        property_types = ["house", "apartment", "condo", "townhouse"]

        name = rng.choice(names)
        property_type = rng.choice(property_types)

        # Scale ranges by difficulty while maintaining integer results
        budget = int(rng.randrange(300000, int(500000 * difficulty), 10000))
        price = int(rng.randrange(250000, budget, 10000))
        brokerage_fee = int(rng.randint(3, 8))
        transfer_fee = int(rng.randint(10, 15))

        # Verify conditions
        while True:
            total_cost = price * (1 + brokerage_fee / 100 + transfer_fee / 100)
            if total_cost > budget + 1 and price * brokerage_fee % 100 == 0 and price * transfer_fee % 100 == 0:
                break
            price = int(rng.randrange(250000, budget, 10000))

        result = generate_from_variables(name, property_type, budget, price, brokerage_fee, transfer_fee)

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