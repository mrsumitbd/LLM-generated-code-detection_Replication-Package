class KeysResourceWithStreamingResponse:
    def __init__(self, keys: "KeysResource") -> None:
        self._keys = keys

    def __getattr__(self, name):
        attr = getattr(self._keys, name)
        if callable(attr):
            def wrapper(*args, **kwargs):
                return attr(*args, **kwargs)
            return wrapper
        return attr