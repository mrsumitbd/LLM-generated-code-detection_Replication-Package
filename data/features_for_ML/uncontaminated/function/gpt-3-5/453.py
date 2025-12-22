def get_least_common_multiple(a: Union[int, float], b: Union[int, float], precision: Optional[float] = 1e-10) -> float:
    def gcd(x, y):
        while y != 0:
            x, y = y, x % y
        return x

    def lcm(x, y):
        return abs(x * y) // gcd(x, y)

    return round(lcm(int(a / precision), int(b / precision)) * precision, 10)