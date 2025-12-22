import pandas as pd
import numpy as np

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
    """
    Quantitative Qualitative Estimation (QQE) indicator.

    Parameters
    ----------
    close : array-like or pd.Series
        Closing price series.
    length : int, optional
        Period for RSI and ATR calculations. Default is 14.
    smooth : int, optional
        Period for smoothing the RSI. Default is 5.
    factor : float, optional
        Multiplier for ATR to determine the threshold. Default is 0.5.
    mamode : str, optional
        Moving‑average mode for smoothing the RSI. Options are
        'ema' (default) or 'sma'.
    drift : int, optional
        Number of periods to shift the result. Default is 0.
    offset : float, optional
        Constant to add to the result. Default is 0.

    Returns
    -------
    pd.Series
        QQE values aligned with the input series.
    """
    # Default values
    length = int(length) if length is not None else 14
    smooth = int(smooth) if smooth is not None else 5
    factor = float(factor) if factor is not None else 0.5
    mamode = mamode if mamode is not None else "ema"
    drift = int(drift) if drift is not None else 0
    offset = float(offset) if offset is not None else 0.0

    close = pd.Series(close).copy()
    close.name = "close"

    # 1. RSI calculation
    delta = close.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    roll_up = up.rolling(window=length, min_periods=1).mean()
    roll_down = down.rolling(window=length, min_periods=1).mean()
    rs = roll_up / roll_down
    rsi = 100 - (100 / (1 + rs))

    # 2. Smooth RSI
    if mamode.lower() == "sma":
        smoothed_rsi = rsi.rolling(window=smooth, min_periods=1).mean()
    else:  # default to EMA
        smoothed_rsi = rsi.ewm(span=smooth, adjust=False).mean()

    # 3. ATR approximation (using close price volatility)
    atr = close.diff().abs().rolling(window=length, min_periods=1).mean()

    # 4. Threshold
    threshold = atr * factor

    # 5. QQE series
    diff = smoothed_rsi.diff()
    qqe_series = pd.Series(index=close.index, dtype=float)

    prev_val = np.nan
    for i in range(len(close)):
        if i == 0:
            qqe_series.iloc[i] = smoothed_rsi.iloc[i]
            prev_val = qqe_series.iloc[i]
        else:
            if diff.iloc[i] > threshold.iloc[i]:
                qqe_series.iloc[i] = smoothed_rsi.iloc[i]
            else:
                qqe_series.iloc[i] = prev_val
            prev_val = qqe_series.iloc[i]

    # 6. Apply drift and offset
    if drift != 0:
        qqe_series = qqe_series.shift(drift)
    if offset != 0.0:
        qqe_series = qqe_series + offset

    qqe_series.name = "qqe"
    return qqe_series