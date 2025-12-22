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
        float: The least common multiple of a and b.
    """
    # Helper to compute integer lcm
    def _int_lcm(x: int, y: int) -> int:
        if x == 0 or y == 0:
            return 0
        return abs(x * y) // math.gcd(x, y)

    # Check if a and b are effectively integers
    def _is_int(val: Union[int, float]) -> bool:
        return isinstance(val, int) or abs(val - round(val)) < precision

    if _is_int(a) and _is_int(b):
        return float(_int_lcm(int(round(a)), int(round(b))))

    # For non-integer values, scale to integers using precision
    a_scaled = int(round(a / precision))
    b_scaled = int(round(b / precision))
    lcm_scaled = _int_lcm(a_scaled, b_scaled)
    return lcm_scaled * precision