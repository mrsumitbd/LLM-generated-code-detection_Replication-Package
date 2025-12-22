import math
from typing import Any

# Try to import pandas for NA handling; fall back to None if not available
try:
    import pandas as pd

    def _is_na(val: Any) -> bool:
        """Return True if val is a pandas NA value."""
        return pd.isna(val)
except Exception:
    # If pandas is not available, treat None as NA
    def _is_na(val: Any) -> bool:
        return val is None


def atan(value: Any) -> Any:
    """
    Returns the arc tangent of a value.

    :param value: A value.
    :return: The arc tangent of the value.
    """
    if _is_na(value):
        # Preserve the NA value (could be pandas.NA or None)
        return value
    # Convert to float and compute atan
    return math.atan(float(value))