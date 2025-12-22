from typing import Iterable

def combine(outcomes: Iterable[Outcome]):
    result = Outcome(0, 0)
    for outcome in outcomes:
        result.wins += outcome.wins
        result.losses += outcome.losses
    return result