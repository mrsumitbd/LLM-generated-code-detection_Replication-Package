from pynecore.types.ohlcv import OHLCV
from .. import lib
from .. import lib
from typing import Iterable, Iterator, Callable, TYPE_CHECKING, Any
from .. import lib
from .. import lib
from types import ModuleType
from datetime import datetime, UTC
from .. import lib

def _set_lib_properties(ohlcv: OHLCV, bar_index: int, tz: 'ZoneInfo', lib: ModuleType):
    """
    Set lib properties from OHLCV
    """
    if TYPE_CHECKING:  # This is needed for the type checker to work
        from .. import lib

    lib.bar_index = lib.last_bar_index = bar_index

    lib.open = _round_price(ohlcv.open, lib)
    lib.high = _round_price(ohlcv.high, lib)
    lib.low = _round_price(ohlcv.low, lib)
    lib.close = _round_price(ohlcv.close, lib)

    lib.volume = ohlcv.volume

    lib.hl2 = (lib.high + lib.low) / 2.0
    lib.hlc3 = (lib.high + lib.low + lib.close) / 3.0
    lib.ohlc4 = (lib.open + lib.high + lib.low + lib.close) / 4.0
    lib.hlcc4 = (lib.high + lib.low + 2 * lib.close) / 4.0

    dt = lib._datetime = datetime.fromtimestamp(ohlcv.timestamp, UTC).astimezone(tz)
    lib._time = lib.last_bar_time = int(dt.timestamp() * 1000)  # PineScript representation of time