from random import Random
from typing import Any

def generate_example(rng: Random, difficulty: float = 1.0) -> dict[str, Any]:
        names_female = ["Emma", "Olivia", "Ava", "Isabella", "Sophia", "Mia", "Charlotte", "Amelia"]
        sports = ["swimming", "cycling", "basketball", "soccer", "volleyball"]
        items1 = ["t-shirt", "jersey", "sports bra"]
        items2 = ["shorts", "leggings", "sweatpants"]
        items3 = ["sneakers", "cleats", "athletic shoes"]
        items4 = ["socks", "headbands", "wristbands"]
        currencies = ["$", "€", "£"]

        name = rng.choice(names_female)
        sport = rng.choice(sports)
        item1 = rng.choice(items1)
        item2 = rng.choice(items2)
        item3 = rng.choice(items3)
        item4 = rng.choice(items4)
        currency = rng.choice(currencies)

        price1 = int(rng.randint(8, int(25 * difficulty)))
        price2 = int(rng.randint(3, int(15 * difficulty)))
        price4 = int(rng.randint(5, int(15 * difficulty)))
        discount = int(rng.randint(1, min(5, price4)))

        # Ensure price3 is even for clean division by 2
        price3 = int(rng.randint(30, int(80 * difficulty)) // 2 * 2)

        result = generate_from_variables(
            name, sport, item1, item2, item3, item4, currency, price1, price2, price3, price4, discount
        )

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