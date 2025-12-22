from typing import List
from async_ohlcv_resource import AsyncOhlcvResource

class AsyncOhlcvResourceWithStreamingResponse:

    def __init__(self, ohlcv: AsyncOhlcvResource) -> None:
        self.ohlcv = ohlcv

    async def get_ohlcv_data(self, symbol: str, timeframe: str, limit: int) -> List[dict]:
        return await self.ohlcv.get_ohlcv_data(symbol, timeframe, limit)

    async def stream_ohlcv_data(self, symbol: str, timeframe: str) -> List[dict]:
        return await self.ohlcv.stream_ohlcv_data(symbol, timeframe)