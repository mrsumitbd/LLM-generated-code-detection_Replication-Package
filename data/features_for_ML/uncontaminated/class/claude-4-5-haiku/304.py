class AsyncTokenPriceResourceWithRawResponse:

    def __init__(self, token_price: AsyncTokenPriceResource) -> None:
        self._token_price = token_price

    def get(
        self,
        token_id: str,
        *,
        vs_currency: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Awaitable[BinaryAPIResponse]:
        return self._token_price.get(
            token_id,
            vs_currency=vs_currency,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )