from functools import reduce
from typing import Any, TypeIs, TypeVar, Iterable

def combine(outcomes: Iterable[Outcome]):
    if not outcomes:
        return Skip()

    combined = reduce(lambda acc, outcome: acc.combine(outcome), outcomes, DepSkip())

    if not isinstance(combined, Ok):
        return combined

    if isinstance(combined.data, _OkData):
        return Ok(data=combined.data.values, location=combined.location)

    # Python will not run reduce if there's a single element in the list, it
    # returns the first element, so the value should be wrapped.
    return Ok(data=[combined.data], location=combined.location)