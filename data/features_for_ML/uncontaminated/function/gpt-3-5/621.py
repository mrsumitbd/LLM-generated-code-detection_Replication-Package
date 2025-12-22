from typing import Iterable

def combine(outcomes: Iterable[Outcome]):
    result = [[]]
    for outcome in outcomes:
        new_result = []
        for prev in result:
            for value in outcome:
                new_result.append(prev + [value])
        result = new_result
    return result