from functools import cached_property

class SimpleResourceWithRawResponse:

    def __init__(self, simple: SimpleResource) -> None:
        pass

    @cached_property
    def price(self) -> PriceResourceWithRawResponse:
        pass

    @cached_property
    def supported_vs_currencies(self) -> SupportedVsCurrenciesResourceWithRawResponse:
        pass

    @cached_property
    def token_price(self) -> TokenPriceResourceWithRawResponse:
        pass