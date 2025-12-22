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
        valid_timeframes = ['1m', '5m', '15m', '30m', '1h', '4h', '1d']
        if self.timeframe not in valid_timeframes:
            raise ValueError("Invalid timeframe specified")

    @classmethod
    @lru_cache(maxsize=128)
    def get_resampler(cls, timeframe: str) -> 'Resampler':
        return cls(timeframe)

    def get_bar_time(self, current_time_ms: int) -> int:
        if self.timeframe == '1m':
            return current_time_ms - (current_time_ms % 60000)
        elif self.timeframe == '5m':
            return current_time_ms - (current_time_ms % 300000)
        elif self.timeframe == '15m':
            return current_time_ms - (current_time_ms % 900000)
        elif self.timeframe == '30m':
            return current_time_ms - (current_time_ms % 1800000)
        elif self.timeframe == '1h':
            return current_time_ms - (current_time_ms % 3600000)
        elif self.timeframe == '4h':
            return current_time_ms - (current_time_ms % 14400000)
        elif self.timeframe == '1d':
            return current_time_ms - (current_time_ms % 86400000)