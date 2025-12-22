from zoneinfo import ZoneInfo
from types import ModuleType
from typing import NamedTuple

class OHLCV(NamedTuple):
    open: float
    high: float
    low: float
    close: float
    volume: float

def _set_lib_properties(ohlcv: OHLCV, bar_index: int, tz: 'ZoneInfo', lib: ModuleType):
    lib.open[bar_index] = ohlcv.open
    lib.high[bar_index] = ohlcv.high
    lib.low[bar_index] = ohlcv.low
    lib.close[bar_index] = ohlcv.close
    lib.volume[bar_index] = ohlcv.volume