import time
from typing import Any

class SyncAPIResource:
    """
    A synchronous wrapper around an asynchronous Reducto client.
    """

    def __init__(self, client: Any) -> None:
        """
        Initialize the resource with a Reducto client.

        Parameters
        ----------
        client : Any
            The underlying Reducto client instance.
        """
        self.client = client

    def _sleep(self, seconds: float) -> None:
        """
        Pause execution for the specified number of seconds.

        Parameters
        ----------
        seconds : float
            The number of seconds to sleep.
        """
        time.sleep(seconds)