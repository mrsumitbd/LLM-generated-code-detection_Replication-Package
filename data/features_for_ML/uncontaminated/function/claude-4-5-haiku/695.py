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
    from pandas import DataFrame
    import talib
    
    # Set defaults
    length = int(length) if length and length > 0 else 14
    smooth = int(smooth) if smooth and smooth > 0 else 5
    factor = float(factor) if factor and factor > 0 else 4.236
    mamode = mamode if mamode else "ema"
    drift = int(drift) if drift and drift != 0 else 1
    offset = int(offset) if offset and offset != 0 else 0
    
    # Validate inputs
    if close is None or len(close) == 0:
        return None
    
    m = close.size
    if m < length:
        return None
    
    # Calculate RSI
    rsi = talib.RSI(close, timeperiod=length)
    
    # Calculate RSI moving average
    if mamode.lower() == "ema":
        rsi_ma = talib.EMA(rsi, timeperiod=smooth)
    elif mamode.lower() == "sma":
        rsi_ma = talib.SMA(rsi, timeperiod=smooth)
    else:
        rsi_ma = talib.EMA(rsi, timeperiod=smooth)
    
    # Calculate RSI standard deviation
    rsi_std = talib.STDDEV(rsi, timeperiod=smooth)
    
    # Calculate upper and lower bands
    upper_band = rsi_ma + (factor * rsi_std)
    lower_band = rsi_ma - (factor * rsi_std)
    
    # Clip bands to 0-100 range
    upper_band = upper_band.clip(lower=0, upper=100)
    lower_band = lower_band.clip(lower=0, upper=100)
    
    # Calculate QQE line
    qqe_line = rsi_ma.copy()
    
    # Calculate fast RSI
    fast_rsi = talib.RSI(close, timeperiod=int(length / 2))
    
    # Create result dataframe
    result = DataFrame({
        "QQE": qqe_line,
        "RSI": rsi,
        "UPPER": upper_band,
        "LOWER": lower_band,
        "FAST_RSI": fast_rsi,
    }, index=close.index)
    
    if offset != 0:
        result = result.shift(offset)
    
    return result