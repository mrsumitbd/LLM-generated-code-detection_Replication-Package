class SyncAPIResource:

    def __init__(self, client: Reducto) -> None:
        self._client = client

    def _sleep(self, seconds: float) -> None:
        import time
        time.sleep(seconds)