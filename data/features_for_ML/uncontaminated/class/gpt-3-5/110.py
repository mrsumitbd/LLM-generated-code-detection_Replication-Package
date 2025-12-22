from typing import List
from async_ohlcv_resource import AsyncOhlcvResource

class AsyncOhlcvResourceWithRawResponse:

    def __init__(self, ohlcv: AsyncOhlcvResource) -> None:
        self.ohlcv = ohlcv

    async def get_ohlcv_data(self) -> List[dict]:
        raw_data = await self.ohlcv.get_raw_data()
        return raw_data