class MarketChartResourceWithStreamingResponse:
    def __init__(self, market_chart: MarketChartResource) -> None:
        self.market_chart = market_chart

    def __getattr__(self, name):
        return getattr(self.market_chart, name)

    def stream(self, *args, **kwargs):
        if hasattr(self.market_chart, "stream"):
            return self.market_chart.stream(*args, **kwargs)
        raise AttributeError("Underlying resource has no 'stream' method")