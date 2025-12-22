import asyncio
from typing import AsyncGenerator

class AsyncTotalSupplyChartResource:
    async def get_total_supply_chart(self) -> dict:
        # Implement the logic to fetch the total supply chart data
        pass

class AsyncTotalSupplyChartResourceWithStreamingResponse:
    def __init__(self, total_supply_chart: AsyncTotalSupplyChartResource) -> None:
        self.total_supply_chart = total_supply_chart

    async def stream_total_supply_chart(self) -> AsyncGenerator[dict, None]:
        while True:
            chart_data = await self.total_supply_chart.get_total_supply_chart()
            yield chart_data
            await asyncio.sleep(5)