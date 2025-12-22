class CoingeckoWithStreamedResponse:

    def __init__(self, client: Coingecko) -> None:
        self._client = client

    def __getattr__(self, name: str):
        original_method = getattr(self._client, name)
        
        if not callable(original_method):
            return original_method
        
        def wrapped_method(*args, **kwargs):
            kwargs['stream'] = True
            return original_method(*args, **kwargs)
        
        return wrapped_method