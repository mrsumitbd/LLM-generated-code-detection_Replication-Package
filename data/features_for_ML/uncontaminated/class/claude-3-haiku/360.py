class TokenListsResourceWithRawResponse:
    def __init__(self, token_lists: TokenListsResource) -> None:
        self.token_lists = token_lists
        self.raw_response = None

    def get_token_lists(self) -> List[TokenList]:
        self.raw_response = self.token_lists.get_token_lists()
        return self.token_lists.get_token_lists()

    def get_token_list(self, token_list_id: str) -> TokenList:
        self.raw_response = self.token_lists.get_token_list(token_list_id)
        return self.token_lists.get_token_list(token_list_id)

    def create_token_list(self, token_list: TokenList) -> TokenList:
        self.raw_response = self.token_lists.create_token_list(token_list)
        return self.token_lists.create_token_list(token_list)

    def update_token_list(self, token_list_id: str, token_list: TokenList) -> TokenList:
        self.raw_response = self.token_lists.update_token_list(token_list_id, token_list)
        return self.token_lists.update_token_list(token_list_id, token_list)

    def delete_token_list(self, token_list_id: str) -> None:
        self.raw_response = self.token_lists.delete_token_list(token_list_id)
        self.token_lists.delete_token_list(token_list_id)