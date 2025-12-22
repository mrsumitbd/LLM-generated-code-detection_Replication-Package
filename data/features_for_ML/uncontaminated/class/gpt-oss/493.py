class MarketChartResourceWithStreamingResponse:
    def __init__(self, market_chart: MarketChartResource) -> None:
        self._market_chart = market_chart

    def __getattr__(self, name):
        return getattr(self._market_chart, name)