from random import Random
from reasoning_gym.utils import format_number, is_integer
from fractions import Fraction
from typing import Any

def generate_example(rng: Random, difficulty: float = 1.0) -> dict[str, Any]:
        names = ["John", "Michael", "David", "James", "William", "Robert", "Joseph"]
        events = ["field trip", "sports tournament", "conference", "music festival", "science fair"]
        organizations = ["school", "community center", "local charity", "youth club", "parent association"]
        currencies = ["$", "€", "£"]
        fractions = ["half", "1/2", "one-half"]

        name = rng.choice(names)
        event = rng.choice(events)
        organization = rng.choice(organizations)
        currency = rng.choice(currencies)
        fraction = rng.choice(fractions)
        fraction = convert_fraction_word(fraction)
        frac_val = Fraction(fraction)

        # Generate total first
        total = int(rng.randrange(200, int(1000 * difficulty), 10))

        # Calculate organization contribution
        org_contribution = int(total * frac_val)

        # Generate current ensuring total contribution doesn't exceed total
        max_current = total - org_contribution - 50  # Leave buffer
        if max_current < 10:  # If not enough room, adjust total up
            total = int((org_contribution + 60) * 1.5)  # Ensure enough space
            org_contribution = int(total * frac_val)
            max_current = total - org_contribution - 50

        current = int(rng.randrange(10, min(int(200 * difficulty), max_current), 5))

        # Verify conditions
        while not is_integer(total * frac_val) or (org_contribution + current >= total):
            total = int(rng.randrange(200, int(1000 * difficulty), 10))
            org_contribution = int(total * frac_val)
            max_current = total - org_contribution - 50
            if max_current < 10:
                total = int((org_contribution + 60) * 1.5)
                org_contribution = int(total * frac_val)
                max_current = total - org_contribution - 50
            current = int(rng.randrange(10, min(int(200 * difficulty), max_current), 5))

        result = generate_from_variables(name, event, organization, fraction, current, total, currency)

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