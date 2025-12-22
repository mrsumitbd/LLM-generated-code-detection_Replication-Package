from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)

class AsyncTotalSupplyChartResourceWithStreamingResponse:
    def __init__(self, total_supply_chart: AsyncTotalSupplyChartResource) -> None:
        self._total_supply_chart = total_supply_chart

        self.get = async_to_streamed_response_wrapper(
            total_supply_chart.get,
        )
        self.get_range = async_to_streamed_response_wrapper(
            total_supply_chart.get_range,
        )