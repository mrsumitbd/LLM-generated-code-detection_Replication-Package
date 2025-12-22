import pandas as pd
import numpy as np
from datetime import datetime
from typing import Optional, Union


class MarketData:
    """Container for market data and analysis."""

    def __init__(self, name: Optional[str] = None):
        self.name = name
        self.df = pd.DataFrame(columns=["timestamp", "price", "volume"])
        self.df["timestamp"] = pd.to_datetime(self.df["timestamp"])

    # ------------------------------------------------------------------
    # Data ingestion
    # ------------------------------------------------------------------
    def add_record(
        self,
        timestamp: Union[str, datetime, pd.Timestamp],
        price: float,
        volume: float = 0.0,
    ) -> None:
        """Add a single market data record."""
        new_row = pd.DataFrame(
            {
                "timestamp": [pd.to_datetime(timestamp)],
                "price": [price],
                "volume": [volume],
            }
        )
        self.df = pd.concat([self.df, new_row], ignore_index=True)
        self._post_process()

    def load_csv(
        self,
        filepath: str,
        timestamp_col: str = "timestamp",
        price_col: str = "price",
        volume_col: str = "volume",
    ) -> None:
        """Load market data from a CSV file."""
        df = pd.read_csv(filepath, parse_dates=[timestamp_col])
        df = df[[timestamp_col, price_col, volume_col]]
        df.columns = ["timestamp", "price", "volume"]
        self.df = pd.concat([self.df, df], ignore_index=True)
        self._post_process()

    def to_csv(self, filepath: str) -> None:
        """Export the market data to a CSV file."""
        self.df.to_csv(filepath, index=False)

    @classmethod
    def from_csv(
        cls,
        filepath: str,
        name: Optional[str] = None,
        timestamp_col: str = "timestamp",
        price_col: str = "price",
        volume_col: str = "volume",
    ) -> "MarketData":
        """Create a MarketData instance from a CSV file."""
        obj = cls(name=name)
        obj.load_csv(filepath, timestamp_col, price_col, volume_col)
        return obj

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _post_process(self) -> None:
        """Sort by timestamp and drop duplicate timestamps."""
        self.df.sort_values("timestamp", inplace=True, ignore_index=True)
        self.df.drop_duplicates(subset="timestamp", keep="last", inplace=True)

    # ------------------------------------------------------------------
    # Basic accessors
    # ------------------------------------------------------------------
    def get_price_series(self) -> pd.Series:
        """Return a pandas Series of prices indexed by timestamp."""
        return self.df.set_index("timestamp")["price"]

    def get_volume_series(self) -> pd.Series:
        """Return a pandas Series of volumes indexed by timestamp."""
        return self.df.set_index("timestamp")["volume"]

    def get_latest_price(self) -> Optional[float]:
        """Return the most recent price."""
        if self.df.empty:
            return None
        return self.df.iloc[-1]["price"]

    def get_latest_volume(self) -> Optional[float]:
        """Return the most recent volume."""
        if self.df.empty:
            return None
        return self.df.iloc[-1]["volume"]

    def get_price_at(self, timestamp: Union[str, datetime, pd.Timestamp]) -> Optional[float]:
        """Return the price at a specific timestamp."""
        ts = pd.to_datetime(timestamp)
        row = self.df[self.df["timestamp"] == ts]
        if row.empty:
            return None
        return row.iloc[0]["price"]

    def get_volume_at(self, timestamp: Union[str, datetime, pd.Timestamp]) -> Optional[float]:
        """Return the volume at a specific timestamp."""
        ts = pd.to_datetime(timestamp)
        row = self.df[self.df["timestamp"] == ts]
        if row.empty:
            return None
        return row.iloc[0]["volume"]

    def get_price_range(
        self,
        start: Union[str, datetime, pd.Timestamp],
        end: Union[str, datetime, pd.Timestamp],
    ) -> pd.Series:
        """Return price series between start and end timestamps."""
        start_ts = pd.to_datetime(start)
        end_ts = pd.to_datetime(end)
        mask = (self.df["timestamp"] >= start_ts) & (self.df["timestamp"] <= end_ts)
        return self.df.loc[mask].set_index("timestamp")["price"]

    def get_volume_range(
        self,
        start: Union[str, datetime, pd.Timestamp],
        end: Union[str, datetime, pd.Timestamp],
    ) -> pd.Series:
        """Return volume series between start and end timestamps."""
        start_ts = pd.to_datetime(start)
        end_ts = pd.to_datetime(end)
        mask = (self.df["timestamp"] >= start_ts) & (self.df["timestamp"] <= end_ts)
        return self.df.loc[mask].set_index("timestamp")["volume"]

    def get_max_price(self) -> Optional[float]:
        """Return the maximum price."""
        return self.df["price"].max() if not self.df.empty else None

    def get_min_price(self) -> Optional[float]:
        """Return the minimum price."""
        return self.df["price"].min() if not self.df.empty else None

    def get_max_volume(self) -> Optional[float]:
        """Return the maximum volume."""
        return self.df["volume"].max() if not self.df.empty else None

    def get_min_volume(self) -> Optional[float]:
        """Return the minimum volume."""
        return self.df["volume"].min() if not self.df.empty else None

    # ------------------------------------------------------------------
    # Analysis helpers
    # ------------------------------------------------------------------
    def compute_sma(self, period: int) -> pd.Series:
        """Compute simple moving average of the price."""
        return self.get_price_series().rolling(window=period, min_periods=1).mean()

    def compute_ema(self, period: int) -> pd.Series:
        """Compute exponential moving average of the price."""
        return self.get_price_series().ewm(span=period, adjust=False, min_periods=1).mean()

    def compute_returns(self) -> pd.Series:
        """Compute daily (or period) returns of the price."""
        return self.get_price_series().pct_change()

    def compute_volatility(self, period: int) -> pd.Series:
        """Compute rolling standard deviation of returns."""
        return self.compute_returns().rolling(window=period, min_periods=1).std()

    def correlation_with(
        self,
        other: "MarketData",
        period: Optional[int] = None,
    ) -> Union[float, pd.Series]:
        """
        Compute correlation between this dataset and another MarketData instance.
        If period is None, compute a single correlation coefficient.
        If period is provided, compute a rolling correlation.
        """
        if not isinstance(other, MarketData):
            raise TypeError("other must be a MarketData instance")

        series1 = self.get_price_series()
        series2 = other.get_price_series()

        if period is None:
            return series1.corr(series2)
        else:
            return series1.rolling(window=period, min_periods=1).corr(series2)

    # ------------------------------------------------------------------
    # Python protocol methods
    # ------------------------------------------------------------------
    def __len__(self) -> int:
        return len(self.df)

    def __repr__(self) -> str:
        name_str = f"'{self.name}'" if self.name else "Unnamed"
        return (
            f"<MarketData {name_str} | "
            f"{len(self.df)} records | "
            f"price: {self.get_min_price():.2f}–{self.get_max_price():.2f} | "
            f"volume: {self.get_min_volume():.2f}–{self.get_max_volume():.2f}>"
        )

    def __iter__(self):
        """Iterate over rows as dictionaries."""
        for _, row in self.df.iterrows():
            yield row.to_dict()