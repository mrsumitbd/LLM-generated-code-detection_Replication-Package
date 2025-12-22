import os
import time
import logging
from typing import Dict
from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.exceptions import CosmosHttpResponseError

MAX_RETRIES = int(os.getenv("MAX_RETRIES", 5))
INITIAL_RETRY_DELAY = 0.5
MAX_RETRY_DELAY = 8

class CosmosDBClient:
    """
    CosmosDBClient uses the Cosmos SDK's retry mechanism with exponential backoff.
    The number of retries is controlled by the MAX_RETRIES environment variable.
    Delays between retries start at 0.5 seconds, doubling up to 8 seconds.
    If a rate limit error occurs after retries, the client will retry once more after the retry-after-ms header duration (if the header is present).
    """

    def __init__(self, config: Configuration = None):
        self.cosmos_client = CosmosClient(
            url=config.cosmos_db_endpoint, credential=config.cosmos_db_key
        )
        self.database = self.cosmos_client.get_database_client(config.cosmos_db_name)

    def get_document(self, container: str, key: str) -> Dict:
        retries = 0
        delay = INITIAL_RETRY_DELAY

        while retries < MAX_RETRIES:
            try:
                container_client = self.database.get_container_client(container)
                return container_client.read_item(item=key)
            except CosmosHttpResponseError as e:
                if e.status_code == 429:  # Rate limit error
                    retry_after_ms = e.headers.get("retry-after-ms")
                    if retry_after_ms:
                        time.sleep(float(retry_after_ms) / 1000)
                        continue
                logging.warning(f"Error getting document: {e}")
                time.sleep(delay)
                delay = min(delay * 2, MAX_RETRY_DELAY)
                retries += 1
        raise Exception("Failed to get document after maximum retries.")

    def create_document(self, container: str, key: str, body: Dict = None) -> Dict:
        retries = 0
        delay = INITIAL_RETRY_DELAY

        while retries < MAX_RETRIES:
            try:
                container_client = self.database.get_container_client(container)
                return container_client.create_item(body or {}, partition_key=PartitionKey(key))
            except CosmosHttpResponseError as e:
                if e.status_code == 429:  # Rate limit error
                    retry_after_ms = e.headers.get("retry-after-ms")
                    if retry_after_ms:
                        time.sleep(float(retry_after_ms) / 1000)
                        continue
                logging.warning(f"Error creating document: {e}")
                time.sleep(delay)
                delay = min(delay * 2, MAX_RETRY_DELAY)
                retries += 1
        raise Exception("Failed to create document after maximum retries.")