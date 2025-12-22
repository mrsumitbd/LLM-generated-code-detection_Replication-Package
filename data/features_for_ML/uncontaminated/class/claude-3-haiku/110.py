class AsyncOhlcvResourceWithRawResponse:
    def __init__(self, ohlcv: AsyncOhlcvResource) -> None:
        self._ohlcv = ohlcv

    async def get_ohlcv(self, symbol: str, interval: str, start_time: int, end_time: int) -> Tuple[pd.DataFrame, dict]:
        response = await self._ohlcv.get_ohlcv(symbol, interval, start_time, end_time)
        return response, response.raw

    async def get_latest_ohlcv(self, symbol: str, interval: str, limit: int) -> Tuple[pd.DataFrame, dict]:
        response = await self._ohlcv.get_latest_ohlcv(symbol, interval, limit)
        return response, response.raw