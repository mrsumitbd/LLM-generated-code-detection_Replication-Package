import numpy as np

def atan(value: TFI | np.ndarray[TFI]) -> float | np.ndarray[float]:
    """
    Returns the arc tangent of a value.

    :param value: A value.
    :return: The arc tangent of the value.
    """
    if isinstance(value, np.ndarray):
        return np.arctan(value)
    else:
        return np.arctan(value)