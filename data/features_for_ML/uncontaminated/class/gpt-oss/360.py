class TokenListsResourceWithRawResponse:
    """
    A thin wrapper around :class:`TokenListsResource` that forwards all attribute
    access to the underlying resource instance. This is useful when the caller
    needs the raw HTTP response objects returned by the underlying methods.
    """

    def __init__(self, token_lists: "TokenListsResource") -> None:
        """
        Initialise the wrapper.

        Parameters
        ----------
        token_lists : TokenListsResource
            The underlying resource instance whose methods will be forwarded.
        """
        self._token_lists = token_lists

    def __getattr__(self, name: str):
        """
        Forward attribute access to the underlying :class:`TokenListsResource`
        instance. If the attribute is callable, a wrapper is returned that
        simply forwards the call.

        Parameters
        ----------
        name : str
            The attribute name to look up.

        Returns
        -------
        Any
            The attribute value from the underlying resource.
        """
        attr = getattr(self._token_lists, name)
        if callable(attr):
            def wrapper(*args, **kwargs):
                return attr(*args, **kwargs)
            return wrapper
        return attr

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} wrapping {self._token_lists!r}>"