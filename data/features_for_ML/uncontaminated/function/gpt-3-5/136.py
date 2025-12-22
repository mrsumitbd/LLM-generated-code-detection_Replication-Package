def atan(value: Union[float, int, None]) -> Union[float, None]:
    if value is None:
        return None
    return math.atan(value)