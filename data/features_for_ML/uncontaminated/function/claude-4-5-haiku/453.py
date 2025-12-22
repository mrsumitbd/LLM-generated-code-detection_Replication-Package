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
    from math import gcd
    
    # Convert to integers by scaling
    # Find the number of decimal places needed
    def to_int(x):
        if isinstance(x, int):
            return x
        # Convert float to integer by multiplying by appropriate power of 10
        s = str(x)
        if 'e' in s.lower():
            # Handle scientific notation
            x_float = float(x)
            # Find decimal places
            decimal_places = len(s.split('.')[-1].split('e')[0]) if '.' in s else 0
            return int(round(x_float * (10 ** decimal_places)))
        else:
            if '.' in s:
                decimal_places = len(s.split('.')[1])
                return int(round(x * (10 ** decimal_places)))
            else:
                return int(x)
    
    # Convert both numbers to integers
    a_int = to_int(a)
    b_int = to_int(b)
    
    # Handle zero cases
    if a_int == 0:
        return float(b_int)
    if b_int == 0:
        return float(a_int)
    
    # Calculate LCM using the formula: LCM(a,b) = (a*b) / GCD(a,b)
    gcd_value = gcd(abs(a_int), abs(b_int))
    lcm = abs(a_int * b_int) // gcd_value
    
    return float(lcm)