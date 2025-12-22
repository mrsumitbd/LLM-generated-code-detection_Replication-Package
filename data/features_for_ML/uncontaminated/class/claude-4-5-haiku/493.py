class MarketChartResourceWithStreamingResponse:

    def __init__(self, market_chart: MarketChartResource) -> None:
        self._market_chart = market_chart

    def __getattr__(self, name: str):
        """Delegate attribute access to the underlying MarketChartResource."""
        return getattr(self._market_chart, name)

    @property
    def market_chart(self) -> MarketChartResource:
        """Return the underlying MarketChartResource instance."""
        return self._market_chart