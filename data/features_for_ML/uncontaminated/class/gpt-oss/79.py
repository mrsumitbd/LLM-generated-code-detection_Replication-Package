import os
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

try:
    from azure.cosmos import CosmosClient, exceptions as cosmos_exceptions
except ImportError:  # pragma: no cover
    # Minimal stubs for environments without the SDK
    class CosmosClient:  # type: ignore
        def __init__(self, *_, **__):  # pragma: no cover
            raise RuntimeError("Azure Cosmos SDK is required")

    class cosmos_exceptions:  # type: ignore
        class CosmosHttpResponseError(Exception):
            def __init__(self, status_code: int, headers: Dict[str, Any]):  # pragma: no cover
                self.status_code = status_code
                self.headers = headers


@dataclass
class Configuration:
    endpoint: str
    key: str
    database_name: str


class CosmosDBClient:
    """
    CosmosDBClient uses the Cosmos SDK's retry mechanism with exponential backoff.
    The number of retries is controlled by the MAX_RETRIES environment variable.
    Delays between retries start at 0.5 seconds, doubling up to 8 seconds.
    If a rate limit error occurs after retries, the client will retry once more after the retry-after-ms header duration (if the header is present).
    """

    def __init__(self, config: Optional[Configuration] = None):
        if config is None:
            config = Configuration(
                endpoint=os.getenv("COSMOS_ENDPOINT", ""),
                key=os.getenv("COSMOS_KEY", ""),
                database_name=os.getenv("COSMOS_DATABASE", ""),
            )
        if not all([config.endpoint, config.key, config.database_name]):
            raise ValueError("Cosmos configuration is incomplete")

        self.client = CosmosClient(config.endpoint, credential=config.key)
        self.database = self.client.get_database_client(config.database_name)

        self.max_retries = int(os.getenv("MAX_RETRIES", "5"))
        self.initial_backoff = 0.5
        self.max_backoff = 8.0

    def _retry_operation(self, operation, *args, **kwargs):
        attempt = 0
        backoff = self.initial_backoff
        last_exception = None

        while attempt <= self.max_retries:
            try:
                return operation(*args, **kwargs)
            except cosmos_exceptions.CosmosHttpResponseError as exc:
                last_exception = exc
                if exc.status_code == 429:  # Rate limit
                    # If we have a Retry-After header, use it
                    retry_after_ms = exc.headers.get("retry-after-ms")
                    if retry_after_ms is not None:
                        wait = int(retry_after_ms) / 1000.0
                    else:
                        wait = backoff
                    time.sleep(wait)
                    # After the max retries, do one final attempt if still 429
                    if attempt == self.max_retries:
                        try:
                            return operation(*args, **kwargs)
                        except cosmos_exceptions.CosmosHttpResponseError as final_exc:
                            raise final_exc
                else:
                    # For non‑429 errors, do not retry
                    raise
            attempt += 1
            backoff = min(backoff * 2, self.max_backoff)

        # If we exit the loop, raise the last exception
        raise last_exception

    def get_document(self, container_name: str, key: str) -> Dict[str, Any]:
        container = self.database.get_container_client(container_name)
        return self._retry_operation(container.read_item, item=key, partition_key=key)

    def create_document(self, container_name: str, key: str, body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        container = self.database.get_container_client(container_name)
        if body is None:
            body = {"id": key}
        else:
            body.setdefault("id", key)
        return self._retry_operation(container.create_item, body=body)