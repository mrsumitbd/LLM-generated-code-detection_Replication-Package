from typing import List
from async_total_supply_chart_resource import AsyncTotalSupplyChartResource

class AsyncTotalSupplyChartResourceWithStreamingResponse:

    def __init__(self, total_supply_chart: AsyncTotalSupplyChartResource) -> None:
        self.total_supply_chart = total_supply_chart

    async def get_data_stream(self) -> List[float]:
        # Implementation to get data stream asynchronously
        pass