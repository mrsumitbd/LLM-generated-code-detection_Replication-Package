import math
from typing import Dict, List, Optional, Union

def get_least_common_multiple(
    a: Union[int, float], b: Union[int, float], precision: Optional[float] = 1e-10
) -> float:
    """Given two real numbers, compute their least common multiple.

    Args:
        a (Union[int, float]): Real number 1.
        b (Union[int, float]): Real number 2.
        precision (Optional[float], optional): To go from float to int. Defaults to 1e-10.

    Returns:
        _type_: _description_
    """
    int_a = int(a / precision)
    int_b = int(b / precision)
    return (a * b) / (math.gcd(int_a, int_b) * precision)