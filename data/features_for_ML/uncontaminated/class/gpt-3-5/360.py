class TokenListsResourceWithRawResponse:

    def __init__(self, token_lists: TokenListsResource) -> None:
        self.token_lists = token_lists

    def get_token_lists(self):
        return self.token_lists.get_token_lists()

    def get_raw_response(self):
        return self.token_lists.get_raw_response()