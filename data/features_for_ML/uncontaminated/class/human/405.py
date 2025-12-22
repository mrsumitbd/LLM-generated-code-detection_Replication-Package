from typing import Any, ClassVar, Dict, List
import pandas as pd

class MarketData:
    """Container for market data and analysis."""
    symbol: str
    asset_type: AssetType
    interval: str
    data: pd.DataFrame
    metadata: Dict[str, Any] = None
    indicators: Dict[str, pd.Series] = None
    fundamental_data: Dict[str, Any] = None
    news_sentiment: Dict[str, Any] = None
    economic_data: Dict[str, Any] = None