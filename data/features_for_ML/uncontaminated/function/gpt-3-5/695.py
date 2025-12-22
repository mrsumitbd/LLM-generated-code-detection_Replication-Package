import numpy as np
import pandas as pd
from talib import EMA

def qqe(
    close,
    length=14,
    smooth=5,
    factor=0.2,
    mamode='EMA',
    drift=1,
    offset=0,
    **kwargs,
):
    def qqe_calculation(close, length, smooth, factor, mamode, drift):
        ema1 = EMA(close, length)
        ema2 = EMA(ema1, length)
        de = factor * EMA(ema2, smooth)
        di = EMA(close, smooth)
        q1 = ema1 + drift * de
        q2 = ema2 + drift * de
        q = q1 - q2
        return q, q1, q2

    q, q1, q2 = qqe_calculation(close, length, smooth, factor, mamode, drift)
    return pd.DataFrame({'QQE': q, 'QQE_1': q1, 'QQE_2': q2})