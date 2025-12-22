class KeysResourceWithStreamingResponse:

    def __init__(self, keys: KeysResource) -> None:
        self._keys = keys

    @property
    def keys(self) -> KeysResource:
        return self._keys

    def __getattr__(self, name: str):
        return getattr(self._keys, name)