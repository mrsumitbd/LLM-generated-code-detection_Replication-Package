from __future__ import annotations

from collections import defaultdict
from math import sqrt
from typing import Any, Dict, Iterable, List, Sequence, Union

# The type of `results` is not strictly defined in the repository.  It can be
# a list/tuple of dictionaries, a dataclass with an `outputs` or `data`
# attribute, or any other iterable of mapping-like objects.  The implementation
# below is intentionally tolerant of these variations.
GenerateOutputs = Union[
    Sequence[Dict[str, Any]],
    Iterable[Dict[str, Any]],
    Any,  # fallback for dataclass-like objects
]


def _iterable_of_dicts(obj: Any) -> Iterable[Dict[str, Any]]:
    """
    Convert *obj* into an iterable of dictionaries.

    The function accepts:
    * a list/tuple of dicts
    * an object with an `outputs` or `data` attribute that is iterable
    * any other iterable of dicts
    """
    if isinstance(obj, (list, tuple)):
        return obj
    if hasattr(obj, "outputs"):
        return getattr(obj, "outputs")
    if hasattr(obj, "data"):
        return getattr(obj, "data")
    # Fallback: try to iterate directly
    try:
        iter(obj)
    except TypeError:
        raise TypeError(
            "results must be an iterable of dictionaries or an object with "
            "an `outputs`/`data` attribute"
        )
    return obj


def _is_numeric(value: Any) -> bool:
    return isinstance(value, (int, float, bool)) and not isinstance(value, bool)


def compute_summary(results: GenerateOutputs) -> Dict[str, Any]:
    """
    Compute aggregated statistics from GenerateOutputs in a format usable by
    templates.

    The function intentionally does not change layout based on dataset size.
    """
    # Convert the input into an iterable of dictionaries
    records = list(_iterable_of_dicts(results))

    summary: Dict[str, Any] = {"total": len(records)}

    if not records:
        return summary

    # Collect values per key
    values_by_key: Dict[str, List[Any]] = defaultdict(list)
    for record in records:
        if not isinstance(record, dict):
            continue
        for k, v in record.items():
            if v is not None:
                values_by_key[k].append(v)

    # Compute statistics per key
    for key, values in values_by_key.items():
        if not values:
            continue

        # Determine if the field is numeric
        numeric_values = [v for v in values if isinstance(v, (int, float, bool))]
        if len(numeric_values) == len(values):
            # All values are numeric
            n = len(numeric_values)
            total = sum(numeric_values)
            mean = total / n
            # Compute standard deviation
            variance = sum((x - mean) ** 2 for x in numeric_values) / n
            std = sqrt(variance)
            summary[key] = {
                "count": n,
                "mean": mean,
                "std": std,
                "min": min(numeric_values),
                "max": max(numeric_values),
            }
        else:
            # Non-numeric field – compute value counts
            counts: Dict[Any, int] = defaultdict(int)
            for v in values:
                counts[v] += 1
            summary[key] = {"counts": dict(counts)}

    return summary