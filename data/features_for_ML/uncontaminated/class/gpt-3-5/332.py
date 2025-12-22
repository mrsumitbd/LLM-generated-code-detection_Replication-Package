from reducto import Reducto
import time

class SyncAPIResource:

    def __init__(self, client: Reducto) -> None:
        self.client = client

    def _sleep(self, seconds: float) -> None:
        time.sleep(seconds)