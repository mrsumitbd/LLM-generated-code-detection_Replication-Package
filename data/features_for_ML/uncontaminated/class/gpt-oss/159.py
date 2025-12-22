import json
from typing import Any, Dict, Iterable, Iterator, Optional

class CoingeckoWithStreamedResponse:
    """
    A wrapper around a Coingecko client that provides streaming access to API responses.
    """

    def __init__(self, client: Any) -> None:
        """
        Initialize the wrapper with an existing Coingecko client instance.

        Parameters
        ----------
        client : Any
            An instance of a Coingecko client that exposes a `session` attribute
            (a `requests.Session` or similar) and a `base_url` attribute.
        """
        self.client = client

    def stream(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        chunk_size: int = 1024,
    ) -> Iterator[bytes]:
        """
        Stream the raw response from the Coingecko API.

        Parameters
        ----------
        endpoint : str
            The API endpoint to call (e.g., '/coins/markets').
        params : dict, optional
            Query parameters to include in the request.
        chunk_size : int, optional
            Number of bytes to read per chunk.

        Yields
        ------
        bytes
            Chunks of the response body.
        """
        url = f"{self.client.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        response = self.client.session.get(url, params=params, stream=True)
        response.raise_for_status()
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                yield chunk

    def stream_json(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Iterator[Any]:
        """
        Stream JSON objects from the Coingecko API. Assumes the response is a JSON array
        or newline-delimited JSON objects.

        Parameters
        ----------
        endpoint : str
            The API endpoint to call.
        params : dict, optional
            Query parameters to include in the request.

        Yields
        ------
        Any
            Parsed JSON objects.
        """
        for line in self.stream(endpoint, params=params, chunk_size=4096):
            try:
                decoded = line.decode("utf-8")
                for obj in decoded.splitlines():
                    if obj.strip():
                        yield json.loads(obj)
            except json.JSONDecodeError:
                # If the entire response is a single JSON array, parse it once
                try:
                    yield json.loads(decoded)
                except json.JSONDecodeError:
                    continue