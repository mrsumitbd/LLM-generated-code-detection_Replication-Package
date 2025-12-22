from typing import Union, Optional
import math

def get_least_common_multiple(
    a: Union[int, float], b: Union[int, float], precision: Optional[float] = 1e-10
) -> float:
    """Given two real numbers, compute their least common multiple.

    Args:
        a (Union[int, float]): Real number 1.
        b (Union[int, float]): Real number 2.
        precision (Optional[float], optional): To go from float to int. Defaults to 1e-10.

    Returns:
        float: The least common multiple of the input numbers.
    """
    a_int = round(a / precision)
    b_int = round(b / precision)
    lcm = abs(a_int * b_int) // math.gcd(a_int, b_int)
    return lcm * precision