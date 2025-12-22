import numpy as np
import pandas as pd

def qqe(
    close,
    length=None,
    smooth=None,
    factor=None,
    mamode=None,
    drift=None,
    offset=None,
    **kwargs,
):
    """Indicator: Quantitative Qualitative Estimation (QQE)"""
    if length is None:
        length = 14
    if smooth is None:
        smooth = 3
    if factor is None:
        factor = 1
    if mamode is None:
        mamode = "ema"
    if drift is None:
        drift = 1
    if offset is None:
        offset = 0

    close = pd.Series(close)

    if mamode == "ema":
        qqe_line = close.ewm(span=length, adjust=False).mean()
    elif mamode == "sma":
        qqe_line = close.rolling(length).mean()
    else:
        raise ValueError("Invalid MA mode. Use 'ema' or 'sma'.")

    qqe_signal = qqe_line.rolling(smooth).mean()
    qqe_hist = (qqe_line - qqe_signal) * factor + offset

    return qqe_line, qqe_signal, qqe_hist