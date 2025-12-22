from typing import Any, Dict, List, Optional
from datetime import datetime

class MarketIntelligence:
    """Container for comprehensive market intelligence."""
    symbol: str
    asset_type: str
    timestamp: datetime
    current_price: float
    market_news: List[MarketNews]
    social_metrics: Dict[str, SocialMetrics]
    fundamental_metrics: Optional[FundamentalMetrics]
    analyst_ratings: Dict[str, Any]
    market_events: List[Dict]
    regulatory_updates: List[Dict]
    competitor_analysis: Dict[str, Any]
    risk_metrics: Dict[str, float]