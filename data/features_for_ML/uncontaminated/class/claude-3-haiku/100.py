from datetime import datetime, timedelta
from functools import lru_cache

class Resampler:
    """
    Resampler class for handling different timeframes and calculating bar times.
    
    This class provides functionality to resample data to different timeframes
    and calculate the opening time of bars for various timeframe specifications.
    """

    def __init__(self, timeframe: str):
        self.timeframe = timeframe
        self._validate_timeframe()

    def _validate_timeframe(self) -> None:
        timeframe_units = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        if not isinstance(self.timeframe, str) or len(self.timeframe) < 2 or self.timeframe[-1] not in timeframe_units:
            raise ValueError("Invalid timeframe format. Expected format: '<number><unit>', e.g., '1m', '5m', '1h', '1d'.")
        try:
            self.interval = int(self.timeframe[:-1])
            self.unit = self.timeframe[-1]
            if self.interval <= 0:
                raise ValueError("Timeframe interval must be a positive integer.")
        except ValueError:
            raise ValueError("Invalid timeframe format. Expected format: '<number><unit>', e.g., '1m', '5m', '1h', '1d'.")

    @classmethod
    @lru_cache(maxsize=128)
    def get_resampler(cls, timeframe: str) -> 'Resampler':
        return cls(timeframe)

    def get_bar_time(self, current_time_ms: int) -> int:
        current_time = datetime.fromtimestamp(current_time_ms / 1000)
        bar_start_time = current_time.replace(
            second=0, microsecond=0
        ) - timedelta(
            seconds=current_time.second,
            minutes=current_time.minute % self.interval,
            hours=current_time.hour % (self.interval if self.unit == "h" else 24),
            days=current_time.day % (1 if self.unit == "d" else 7)
        )
        return int(bar_start_time.timestamp() * 1000)