def todegrees(angle: TFI | NA[TFI]) -> float | NA[float]:
    """
    Converts an angle from radians to degrees.

    :param angle: An angle in radians.
    :return: The angle in degrees.
    """
    import math
    
    if isinstance(angle, NA):
        return NA(math.degrees(angle.value))
    else:
        return math.degrees(angle)