class TokenListsResourceWithRawResponse:

    def __init__(self, token_lists: TokenListsResource) -> None:
        self._token_lists = token_lists

    def retrieve(
        self,
        token_list_id: str,
        **kwargs,
    ) -> BinaryAPIResponse:
        extra_headers = {"Accept": "application/json", **kwargs.pop("headers", {})}

        return self._token_lists._client.get(
            f"/token_lists/{token_list_id}",
            options=make_request_options(extra_headers=extra_headers, **kwargs),
            cast_to=TokenList,
        )

    def list(
        self,
        **kwargs,
    ) -> BinaryAPIResponse:
        extra_headers = {"Accept": "application/json", **kwargs.pop("headers", {})}

        return self._token_lists._client.get(
            "/token_lists",
            options=make_request_options(extra_headers=extra_headers, **kwargs),
            cast_to=SyncPage[TokenList],
        )

    def create(
        self,
        *,
        name: str,
        description: str | NotGiven = NOT_GIVEN,
        tokens: Iterable[str] | NotGiven = NOT_GIVEN,
        **kwargs,
    ) -> BinaryAPIResponse:
        extra_headers = {"Accept": "application/json", **kwargs.pop("headers", {})}

        body = make_request_body(
            name=name,
            description=description,
            tokens=tokens,
        )

        return self._token_lists._client.post(
            "/token_lists",
            body=body,
            options=make_request_options(extra_headers=extra_headers, **kwargs),
            cast_to=TokenList,
        )

    def update(
        self,
        token_list_id: str,
        *,
        name: str | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        tokens: Iterable[str] | NotGiven = NOT_GIVEN,
        **kwargs,
    ) -> BinaryAPIResponse:
        extra_headers = {"Accept": "application/json", **kwargs.pop("headers", {})}

        body = make_request_body(
            name=name,
            description=description,
            tokens=tokens,
        )

        return self._token_lists._client.patch(
            f"/token_lists/{token_list_id}",
            body=body,
            options=make_request_options(extra_headers=extra_headers, **kwargs),
            cast_to=TokenList,
        )

    def delete(
        self,
        token_list_id: str,
        **kwargs,
    ) -> BinaryAPIResponse:
        extra_headers = {"Accept": "application/json", **kwargs.pop("headers", {})}

        return self._token_lists._client.delete(
            f"/token_lists/{token_list_id}",
            options=make_request_options(extra_headers=extra_headers, **kwargs),
        )