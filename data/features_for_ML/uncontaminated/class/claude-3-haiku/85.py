import asyncio
from typing import AsyncGenerator

class AsyncOhlcvResourceWithStreamingResponse:
    def __init__(self, ohlcv: AsyncOhlcvResource) -> None:
        self.ohlcv = ohlcv

    async def get_ohlcv(self, symbol: str, interval: str, limit: int = 100, start_time: int = None, end_time: int = None) -> AsyncGenerator[dict, None]:
        async for data in self.ohlcv.get_ohlcv(symbol, interval, limit, start_time, end_time):
            yield data

    async def get_ohlcv_stream(self, symbol: str, interval: str) -> AsyncGenerator[dict, None]:
        async for data in self.ohlcv.get_ohlcv_stream(symbol, interval):
            yield data