from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)

class AsyncCategoriesResourceWithRawResponse:
    def __init__(self, categories: AsyncCategoriesResource) -> None:
        self._categories = categories

        self.get = async_to_raw_response_wrapper(
            categories.get,
        )
        self.get_list = async_to_raw_response_wrapper(
            categories.get_list,
        )