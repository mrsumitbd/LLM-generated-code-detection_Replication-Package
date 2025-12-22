def _set_lib_properties(ohlcv: OHLCV, bar_index: int, tz: 'ZoneInfo', lib: ModuleType):
    """
    Set lib properties from OHLCV
    """
    lib.open = ohlcv.open[bar_index]
    lib.high = ohlcv.high[bar_index]
    lib.low = ohlcv.low[bar_index]
    lib.close = ohlcv.close[bar_index]
    lib.volume = ohlcv.volume[bar_index]
    lib.timestamp = ohlcv.timestamp[bar_index].astimezone(tz)