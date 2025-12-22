class AsyncOhlcvResourceWithRawResponse:

    def __init__(self, ohlcv: AsyncOhlcvResource) -> None:
        self._ohlcv = ohlcv

    async def list(
        self,
        *,
        symbol: str,
        timeframe: str,
        limit: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given to the extra_headers and extra_query parameters will not be stripped
        # so it's possible to pass unrecognized parameters using the extra_* parameters.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        Get OHLCV data for a symbol.

        Args:
          symbol: The symbol to get OHLCV data for (e.g. BTC/USD)

          timeframe: The timeframe for the OHLCV data (e.g. 1m, 5m, 1h, 1d)

          limit: The maximum number of OHLCV candles to return (default 100, max 1000)

          extra_headers: Send extra headers to the request or remove header by setting the
              value to `None`. See also [request options](https://www.httpx.org/api/#request-options).

          extra_query: Add additional query parameters to the request. See also
              [query parameters](https://www.httpx.org/api/#query-parameters).

          extra_body: Add additional JSON properties to the request body. See also
              [request body](https://www.httpx.org/api/#request-content).

          timeout: Override the client-level default request timeout, in seconds. See also [request options](https://www.httpx.org/api/#timeouts).

        Returns:
          Response with raw bytes content
        """
        return await self._ohlcv.list(
            symbol=symbol,
            timeframe=timeframe,
            limit=limit,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )