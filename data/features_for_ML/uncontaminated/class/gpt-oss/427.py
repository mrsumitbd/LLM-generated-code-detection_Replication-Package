class AsyncTotalSupplyChartResourceWithStreamingResponse:
    def __init__(self, total_supply_chart: AsyncTotalSupplyChartResource) -> None:
        self._resource = total_supply_chart
        for attr_name in dir(total_supply_chart):
            if attr_name.startswith("_"):
                continue
            attr = getattr(total_supply_chart, attr_name)
            if callable(attr):
                setattr(self, attr_name, attr)