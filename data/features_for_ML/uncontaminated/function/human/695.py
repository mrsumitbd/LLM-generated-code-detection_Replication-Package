from numpy import maximum as npMaximum
from .rsi import rsi
from pandas import DataFrame, Series
from numpy import minimum as npMinimum
from numpy import nan as npNaN
from pandas_ta_classic.overlap import ma
from pandas_ta_classic.utils import get_drift, get_offset, verify_series

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
    # Validate arguments
    length = int(length) if length and length > 0 else 14
    smooth = int(smooth) if smooth and smooth > 0 else 5
    factor = float(factor) if factor else 4.236
    wilders_length = 2 * length - 1
    mamode = mamode if isinstance(mamode, str) else "ema"
    close = verify_series(close, max(length, smooth, wilders_length))
    drift = get_drift(drift)
    offset = get_offset(offset)

    if close is None:
        return

    # Calculate Result
    rsi_ = rsi(close, length)
    _mode = mamode.lower()[0] if mamode != "ema" else ""
    rsi_ma = ma(mamode, rsi_, length=smooth)

    # RSI MA True Range
    rsi_ma_tr = rsi_ma.diff(drift).abs()

    # Double Smooth the RSI MA True Range using Wilder's Length with a default
    # width of 4.236.
    smoothed_rsi_tr_ma = ma("ema", rsi_ma_tr, length=wilders_length)
    dar = factor * ma("ema", smoothed_rsi_tr_ma, length=wilders_length)

    # Create the Upper and Lower Bands around RSI MA.
    upperband = rsi_ma + dar
    lowerband = rsi_ma - dar

    m = close.size
    long = Series(0, index=close.index)
    short = Series(0, index=close.index)
    trend = Series(1, index=close.index)
    qqe = Series(rsi_ma.iloc[0], index=close.index)
    qqe_long = Series(npNaN, index=close.index)
    qqe_short = Series(npNaN, index=close.index)

    for i in range(1, m):
        c_rsi, p_rsi = rsi_ma.iloc[i], rsi_ma.iloc[i - 1]
        c_long, p_long = long.iloc[i - 1], long.iloc[i - 2]
        c_short, p_short = short.iloc[i - 1], short.iloc[i - 2]

        # Long Line
        if p_rsi > c_long and c_rsi > c_long:
            long.iloc[i] = npMaximum(c_long, lowerband.iloc[i])
        else:
            long.iloc[i] = lowerband.iloc[i]

        # Short Line
        if p_rsi < c_short and c_rsi < c_short:
            short.iloc[i] = npMinimum(c_short, upperband.iloc[i])
        else:
            short.iloc[i] = upperband.iloc[i]

        # Trend & QQE Calculation
        # Long: Current RSI_MA value Crosses the Prior Short Line Value
        # Short: Current RSI_MA Crosses the Prior Long Line Value
        if (c_rsi > c_short and p_rsi < p_short) or (
            c_rsi <= c_short and p_rsi >= p_short
        ):
            trend.iloc[i] = 1
            qqe.iloc[i] = qqe_long.iloc[i] = long.iloc[i]
        elif (c_rsi > c_long and p_rsi < p_long) or (
            c_rsi <= c_long and p_rsi >= p_long
        ):
            trend.iloc[i] = -1
            qqe.iloc[i] = qqe_short.iloc[i] = short.iloc[i]
        else:
            trend.iloc[i] = trend.iloc[i - 1]
            if trend.iloc[i] == 1:
                qqe.iloc[i] = qqe_long.iloc[i] = long.iloc[i]
            else:
                qqe.iloc[i] = qqe_short.iloc[i] = short.iloc[i]

    # Offset
    if offset != 0:
        rsi_ma = rsi_ma.shift(offset)
        qqe = qqe.shift(offset)
        long = long.shift(offset)
        short = short.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        rsi_ma.fillna(kwargs["fillna"], inplace=True)
        qqe.fillna(kwargs["fillna"], inplace=True)
        qqe_long.fillna(kwargs["fillna"], inplace=True)
        qqe_short.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        if "fill_method" in kwargs:

            if kwargs["fill_method"] == "ffill":

                rsi_ma.ffill(inplace=True)

            elif kwargs["fill_method"] == "bfill":

                rsi_ma.bfill(inplace=True)
        if "fill_method" in kwargs:

            if kwargs["fill_method"] == "ffill":

                qqe.ffill(inplace=True)

            elif kwargs["fill_method"] == "bfill":

                qqe.bfill(inplace=True)
        if "fill_method" in kwargs:

            if kwargs["fill_method"] == "ffill":

                qqe_long.ffill(inplace=True)

            elif kwargs["fill_method"] == "bfill":

                qqe_long.bfill(inplace=True)
        if "fill_method" in kwargs:

            if kwargs["fill_method"] == "ffill":

                qqe_short.ffill(inplace=True)

            elif kwargs["fill_method"] == "bfill":

                qqe_short.bfill(inplace=True)

    # Name and Categorize it
    _props = f"{_mode}_{length}_{smooth}_{factor}"
    qqe.name = f"QQE{_props}"
    rsi_ma.name = f"QQE{_props}_RSI{_mode.upper()}MA"
    qqe_long.name = f"QQEl{_props}"
    qqe_short.name = f"QQEs{_props}"
    qqe.category = rsi_ma.category = "momentum"
    qqe_long.category = qqe_short.category = qqe.category

    # Prepare DataFrame to return
    data = {
        qqe.name: qqe,
        rsi_ma.name: rsi_ma,
        # long.name: long, short.name: short
        qqe_long.name: qqe_long,
        qqe_short.name: qqe_short,
    }
    df = DataFrame(data)
    df.name = f"QQE{_props}"
    df.category = qqe.category

    return df