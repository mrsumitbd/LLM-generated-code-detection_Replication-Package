def _set_lib_properties(ohlcv: OHLCV, bar_index: int, tz: 'ZoneInfo', lib: ModuleType):
    """
    Set lib properties from OHLCV
    """
    bar = ohlcv.bars[bar_index]
    
    lib.open = bar.open
    lib.high = bar.high
    lib.low = bar.low
    lib.close = bar.close
    lib.volume = bar.volume
    
    lib.bar_index = bar_index
    lib.time = bar.time.astimezone(tz) if bar.time else None