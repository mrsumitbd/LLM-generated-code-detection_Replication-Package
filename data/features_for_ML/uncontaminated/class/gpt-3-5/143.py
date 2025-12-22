from typing import Dict, Any, List

class AnalyticsStatisticsService:
    """Service for aggregated statistics and analytics"""

    def _build_filters(self, search_params: Dict[str, Any]) -> List:
        filters = []
        for key, value in search_params.items():
            filters.append(f"{key}={value}")
        return filters