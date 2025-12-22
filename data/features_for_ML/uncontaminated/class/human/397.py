from .price import (
    PriceResource,
    AsyncPriceResource,
    PriceResourceWithRawResponse,
    AsyncPriceResourceWithRawResponse,
    PriceResourceWithStreamingResponse,
    AsyncPriceResourceWithStreamingResponse,
)
from .supported_vs_currencies import (
    SupportedVsCurrenciesResource,
    AsyncSupportedVsCurrenciesResource,
    SupportedVsCurrenciesResourceWithRawResponse,
    AsyncSupportedVsCurrenciesResourceWithRawResponse,
    SupportedVsCurrenciesResourceWithStreamingResponse,
    AsyncSupportedVsCurrenciesResourceWithStreamingResponse,
)
from .token_price import (
    TokenPriceResource,
    AsyncTokenPriceResource,
    TokenPriceResourceWithRawResponse,
    AsyncTokenPriceResourceWithRawResponse,
    TokenPriceResourceWithStreamingResponse,
    AsyncTokenPriceResourceWithStreamingResponse,
)
from ..._compat import cached_property

class SimpleResourceWithRawResponse:
    def __init__(self, simple: SimpleResource) -> None:
        self._simple = simple

    @cached_property
    def price(self) -> PriceResourceWithRawResponse:
        return PriceResourceWithRawResponse(self._simple.price)

    @cached_property
    def supported_vs_currencies(self) -> SupportedVsCurrenciesResourceWithRawResponse:
        return SupportedVsCurrenciesResourceWithRawResponse(self._simple.supported_vs_currencies)

    @cached_property
    def token_price(self) -> TokenPriceResourceWithRawResponse:
        return TokenPriceResourceWithRawResponse(self._simple.token_price)