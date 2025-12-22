import math
from ..types.na import NA

def todegrees(angle: TFI | NA[TFI]) -> float | NA[float]:
    """
    Converts an angle from radians to degrees.

    :param angle: An angle in radians.
    :return: The angle in degrees.
    """
    if isinstance(angle, NA):
        return NA(float)
    return math.degrees(angle)