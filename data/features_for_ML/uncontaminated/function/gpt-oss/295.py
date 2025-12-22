from typing import Optional

# The NA type is used in this project to represent missing values.
# If it is not defined elsewhere, we fall back to None.
try:
    from .na import NA  # type: ignore
except Exception:
    NA = None  # type: ignore

def obv() -> float | NA:
    """
    On Balance Volume.

    :return: On Balance Volume or NA if insufficient data.
    """
    # Retrieve global price and volume series
    try:
        close = globals()["close"]
        volume = globals()["volume"]
    except KeyError:
        return NA

    # Ensure we have at least two data points
    if len(close) < 2 or len(volume) < 2:
        return NA

    obv_value = 0.0
    for i in range(1, len(close)):
        if close[i] > close[i - 1]:
            obv_value += volume[i]
        elif close[i] < close[i - 1]:
            obv_value -= volume[i]
        # If close[i] == close[i-1], obv_value remains unchanged

    return obv_value