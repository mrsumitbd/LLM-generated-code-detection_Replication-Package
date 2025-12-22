class AsyncTotalSupplyChartResourceWithStreamingResponse:

    def __init__(self, total_supply_chart: AsyncTotalSupplyChartResource) -> None:
        self._total_supply_chart = total_supply_chart

    def __getattr__(self, name: str):
        return getattr(self._total_supply_chart, name)