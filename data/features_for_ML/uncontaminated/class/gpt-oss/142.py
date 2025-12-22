class AsyncModelsResourceWithRawResponse:
    """
    A wrapper around :class:`AsyncModelsResource` that exposes the same API but
    returns the raw HTTP responses instead of parsed objects.
    """

    def __init__(self, models: "AsyncModelsResource") -> None:
        """
        Initialize the wrapper with an existing :class:`AsyncModelsResource` instance.

        Parameters
        ----------
        models : AsyncModelsResource
            The underlying async models resource to wrap.
        """
        self._models = models

    def __getattr__(self, name: str):
        """
        Delegate attribute access to the underlying :class:`AsyncModelsResource`.

        If the attribute is a coroutine function, wrap it so that it can be awaited
        and the raw response is returned unchanged.

        Parameters
        ----------
        name : str
            The attribute name to retrieve.

        Returns
        -------
        Any
            The attribute from the underlying resource, wrapped if necessary.
        """
        attr = getattr(self._models, name)

        if callable(attr):
            async def wrapper(*args, **kwargs):
                return await attr(*args, **kwargs)

            return wrapper

        return attr