class MarketChartResourceWithStreamingResponse:
    def __init__(self, market_chart: MarketChartResource) -> None:
        self.market_chart = market_chart

    def get_chart_data(self, symbol: str, interval: str, days: int) -> Generator[ChartData, None, None]:
        chart_data = self.market_chart.get_chart_data(symbol, interval, days)
        for data_point in chart_data:
            yield data_point

    def get_chart_data_as_list(self, symbol: str, interval: str, days: int) -> List[ChartData]:
        return list(self.get_chart_data(symbol, interval, days))