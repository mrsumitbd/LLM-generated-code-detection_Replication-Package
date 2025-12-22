from ..types import Series, Persistent, NA
from pynecore.lib import open, high, low, close, volume, hl2, bar_index, array, session, math as lib_math

def obv() -> float | NA[float]:
    """
    On Balance Volume.

    :return: On Balance Volume
    """
    chg = change(close)
    if isinstance(chg, NA):
        return NA(float)
    if chg > 0:
        chg = 1.0
    elif chg < 0:
        chg = -1.0
    else:
        chg = 0.0
    return cum(volume * chg)