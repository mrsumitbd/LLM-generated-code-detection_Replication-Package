from datetime import datetime
from types import ModuleType
from zoneinfo import ZoneInfo

def _set_lib_properties(ohlcv: 'OHLCV', bar_index: int, tz: 'ZoneInfo', lib: ModuleType):
    """
    Set lib properties from OHLCV
    """
    # Common OHLCV attributes
    attrs = ['open', 'high', 'low', 'close', 'volume', 'timestamp']
    for attr in attrs:
        if hasattr(ohlcv, attr):
            value = getattr(ohlcv, attr)
            if attr == 'timestamp':
                # Convert to timezone-aware datetime
                try:
                    # Assume timestamp is in seconds
                    dt = datetime.fromtimestamp(value, tz)
                except Exception:
                    # Fallback: if already datetime
                    dt = value if isinstance(value, datetime) else None
                setattr(lib, 'timestamp', dt)
                setattr(lib, 'datetime', dt)
            else:
                setattr(lib, attr, value)

    # Additional properties
    setattr(lib, 'bar_index', bar_index)
    setattr(lib, 'tz', tz)