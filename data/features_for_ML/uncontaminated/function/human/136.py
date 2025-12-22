import math
from ..types.na import NA

def atan(value: TFI | NA[TFI]) -> float | NA[float]:
    """
    Returns the arc tangent of a value.

    :param value: A value.
    :return: The arc tangent of the value.
    """
    if isinstance(value, NA):
        return NA(float)
    return math.atan(value)