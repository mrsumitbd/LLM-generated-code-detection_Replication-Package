from typing import Union, Optional

TFI = Union[float, int]
NA = Optional

def todegrees(angle: TFI | NA[TFI]) -> float | NA[float]:
    """
    Converts an angle from radians to degrees.

    :param angle: An angle in radians.
    :return: The angle in degrees.
    """
    if angle is None:
        return None
    else:
        return angle * 180 / 3.14159265