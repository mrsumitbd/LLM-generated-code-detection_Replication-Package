import math
from typing import Union, TypeVar

TFI = TypeVar('TFI', int, float)

def atan(value: Union[TFI, 'NA[TFI]']) -> Union[float, 'NA[float]']:
    """
    Returns the arc tangent of a value.

    :param value: A value.
    :return: The arc tangent of the value.
    """
    if isinstance(value, NA):
        return NA(math.atan(value.value))
    return math.atan(value)