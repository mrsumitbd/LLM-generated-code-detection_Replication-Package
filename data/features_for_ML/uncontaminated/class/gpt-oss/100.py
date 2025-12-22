import re
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from typing import ClassVar


class Resampler:
    """
    Resampler class for handling different timeframes and calculating bar times.
    
    This class provides functionality to resample data to different timeframes
    and calculate the opening time of bars for various timeframe specifications.
    """

    _TIMEFRAME_RE: ClassVar[re.Pattern] = re.compile(r"^(\d+)([smhdwMy])$")

    def __init__(self, timeframe: str):
        self.timeframe = timeframe
        self.multiplier, self.unit = self._parse_timeframe(timeframe)
        self._validate_timeframe()

    def _parse_timeframe(self, timeframe: str):
        match = self._TIMEFRAME_RE.match(timeframe)
        if not match:
            raise ValueError(f"Invalid timeframe format: {timeframe}")
        return int(match.group(1)), match.group(2)

    def _validate_timeframe(self) -> None:
        if self.unit not in {"s", "m", "h", "d", "w", "M", "Y"}:
            raise ValueError(f"Unsupported timeframe unit: {self.unit}")

    @classmethod
    @lru_cache(maxsize=128)
    def get_resampler(cls, timeframe: str) -> "Resampler":
        return cls(timeframe)

    def get_bar_time(self, current_time_ms: int) -> int:
        """
        Return the start time (in ms) of the bar that contains the given timestamp.
        """
        dt = datetime.fromtimestamp(current_time_ms / 1000, tz=timezone.utc)

        if self.unit == "s":
            period = timedelta(seconds=self.multiplier)
            bar_start = dt - timedelta(seconds=dt.second % self.multiplier,
                                       microseconds=dt.microsecond)
        elif self.unit == "m":
            period = timedelta(minutes=self.multiplier)
            bar_start = dt - timedelta(minutes=dt.minute % self.multiplier,
                                       seconds=dt.second,
                                       microseconds=dt.microsecond)
        elif self.unit == "h":
            period = timedelta(hours=self.multiplier)
            bar_start = dt - timedelta(hours=dt.hour % self.multiplier,
                                       minutes=dt.minute,
                                       seconds=dt.second,
                                       microseconds=dt.microsecond)
        elif self.unit == "d":
            period = timedelta(days=self.multiplier)
            bar_start = dt.replace(hour=0, minute=0, second=0, microsecond=0)
            # Adjust for multiplier > 1
            days_to_subtract = (dt.day - 1) % self.multiplier
            bar_start -= timedelta(days=days_to_subtract)
        elif self.unit == "w":
            # Week starts on Monday
            weekday = dt.isoweekday()  # Monday=1
            bar_start = dt - timedelta(days=weekday - 1,
                                       hours=dt.hour,
                                       minutes=dt.minute,
                                       seconds=dt.second,
                                       microseconds=dt.microsecond)
            # Adjust for multiplier > 1
            weeks_to_subtract = ((dt.isocalendar()[1] - 1) % self.multiplier)
            bar_start -= timedelta(weeks=weeks_to_subtract)
        elif self.unit == "M":
            bar_start = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        elif self.unit == "Y":
            bar_start = dt.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            raise ValueError(f"Unsupported timeframe unit: {self.unit}")

        return int(bar_start.timestamp() * 1000)