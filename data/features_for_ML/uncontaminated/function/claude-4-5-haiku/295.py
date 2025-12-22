def obv() -> float | NA[float]:
    """
    On Balance Volume.

    :return: On Balance Volume
    """
    from .core import ta
    
    if len(ta.close) == 0:
        return NA(float)
    
    obv_value = 0.0
    
    for i in range(len(ta.close)):
        if i == 0:
            if ta.close[i] > 0:
                obv_value = ta.volume[i]
            else:
                obv_value = 0.0
        else:
            if ta.close[i] > ta.close[i-1]:
                obv_value += ta.volume[i]
            elif ta.close[i] < ta.close[i-1]:
                obv_value -= ta.volume[i]
    
    return obv_value