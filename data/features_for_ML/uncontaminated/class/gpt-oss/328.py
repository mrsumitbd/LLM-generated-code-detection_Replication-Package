class AsyncTokenPriceResourceWithStreamingResponse:
    def __init__(self, token_price: "AsyncTokenPriceResource") -> None:
        self._token_price = token_price

    def __getattr__(self, name):
        # Delegate attribute access to the underlying AsyncTokenPriceResource instance.
        return getattr(self._token_price, name)