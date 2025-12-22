from functools import lru_cache
from datetime import datetime, timedelta
import re

class Resampler:
    """
    Resampler class for handling different timeframes and calculating bar times.
    
    This class provides functionality to resample data to different timeframes
    and calculate the opening time of bars for various timeframe specifications.
    """

    _VALID_UNITS = {'s', 'm', 'h', 'd', 'w', 'M'}
    _UNIT_TO_MS = {
        's': 1000,
        'm': 60 * 1000,
        'h': 60 * 60 * 1000,
        'd': 24 * 60 * 60 * 1000,
        'w': 7 * 24 * 60 * 60 * 1000,
        'M': 30 * 24 * 60 * 60 * 1000,
    }

    def __init__(self, timeframe: str):
        self.timeframe = timeframe
        self._validate_timeframe()
        self._parse_timeframe()

    def _parse_timeframe(self) -> None:
        match = re.match(r'^(\d+)([smhdwM])$', self.timeframe)
        if match:
            self.value = int(match.group(1))
            self.unit = match.group(2)
            self.milliseconds = self.value * self._UNIT_TO_MS[self.unit]
        else:
            raise ValueError(f"Invalid timeframe format: {self.timeframe}")

    def _validate_timeframe(self) -> None:
        if not isinstance(self.timeframe, str):
            raise TypeError("Timeframe must be a string")
        
        match = re.match(r'^(\d+)([smhdwM])$', self.timeframe)
        if not match:
            raise ValueError(f"Invalid timeframe format: {self.timeframe}. Expected format: <number><unit> (e.g., '5m', '1h')")
        
        value, unit = match.groups()
        if unit not in self._VALID_UNITS:
            raise ValueError(f"Invalid timeframe unit: {unit}. Must be one of {self._VALID_UNITS}")
        
        if int(value) <= 0:
            raise ValueError(f"Timeframe value must be positive, got: {value}")

    @classmethod
    @lru_cache(maxsize=128)
    def get_resampler(cls, timeframe: str) -> 'Resampler':
        return cls(timeframe)

    def get_bar_time(self, current_time_ms: int) -> int:
        if not isinstance(current_time_ms, int):
            raise TypeError("current_time_ms must be an integer")
        
        if current_time_ms < 0:
            raise ValueError("current_time_ms must be non-negative")
        
        if self.unit == 'M':
            dt = datetime.utcfromtimestamp(current_time_ms / 1000)
            month_start = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            months_diff = (dt.year - month_start.year) * 12 + (dt.month - month_start.month)
            bar_month = months_diff // self.value
            target_month = month_start.month + bar_month * self.value
            target_year = month_start.year + (target_month - 1) // 12
            target_month = ((target_month - 1) % 12) + 1
            bar_dt = month_start.replace(year=target_year, month=target_month)
            return int(bar_dt.timestamp() * 1000)
        
        elif self.unit == 'w':
            epoch = datetime.utcfromtimestamp(0)
            current_dt = datetime.utcfromtimestamp(current_time_ms / 1000)
            days_since_epoch = (current_dt.replace(hour=0, minute=0, second=0, microsecond=0) - epoch.replace(hour=0, minute=0, second=0, microsecond=0)).days
            weeks_since_epoch = days_since_epoch // 7
            bar_week = weeks_since_epoch // self.value
            bar_days = bar_week * self.value * 7
            bar_dt = epoch + timedelta(days=bar_days)
            return int(bar_dt.timestamp() * 1000)
        
        elif self.unit == 'd':
            dt = datetime.utcfromtimestamp(current_time_ms / 1000)
            epoch = datetime.utcfromtimestamp(0)
            days_since_epoch = (dt.replace(hour=0, minute=0, second=0, microsecond=0) - epoch.replace(hour=0, minute=0, second=0, microsecond=0)).days
            bar_day = days_since_epoch // self.value
            bar_days = bar_day * self.value
            bar_dt = epoch + timedelta(days=bar_days)
            return int(bar_dt.timestamp() * 1000)
        
        else:
            bar_time_ms = (current_time_ms // self.milliseconds) * self.milliseconds
            return bar_time_ms