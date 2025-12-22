import math
from typing import Union

# Import NA from pandas if available; otherwise define a simple sentinel.
try:
    from pandas import NA
except Exception:
    class _NA:
        def __repr__(self):
            return "NA"
    NA = _NA()

def todegrees(angle: Union[float, int, NA]) -> Union[float, NA]:
    """
    Converts an angle from radians to degrees.

    :param angle: An angle in radians.
    :return: The angle in degrees.
    """
    if angle is NA:
        return NA
    # Ensure the input is a numeric type
    try:
        rad = float(angle)
    except (TypeError, ValueError):
        raise TypeError(f"Expected a numeric value or NA, got {type(angle).__name__}")
    return rad * 180.0 / math.pi