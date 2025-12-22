from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)

class TokenListsResourceWithRawResponse:
    def __init__(self, token_lists: TokenListsResource) -> None:
        self._token_lists = token_lists

        self.get_all_json = to_raw_response_wrapper(
            token_lists.get_all_json,
        )