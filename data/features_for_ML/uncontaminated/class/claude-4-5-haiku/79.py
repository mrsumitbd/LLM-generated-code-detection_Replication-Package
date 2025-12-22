import os
import time
from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.exceptions import CosmosHttpResponseError

class CosmosDBClient:
    """
    CosmosDBClient uses the Cosmos SDK's retry mechanism with exponential backoff.
    The number of retries is controlled by the MAX_RETRIES environment variable.
    Delays between retries start at 0.5 seconds, doubling up to 8 seconds.
    If a rate limit error occurs after retries, the client will retry once more after the retry-after-ms header duration (if the header is present).
    """

    def __init__(self, config: 'Configuration' = None):
        self.config = config
        self.max_retries = int(os.getenv('MAX_RETRIES', '3'))
        self.initial_delay = 0.5
        self.max_delay = 8
        
        if config:
            self.client = CosmosClient(config.connection_string)
            self.database = self.client.get_database_client(config.database_name)
        else:
            self.client = None
            self.database = None

    def get_document(self, container, key) -> dict:
        if not self.database:
            raise ValueError("CosmosDBClient not properly initialized")
        
        container_client = self.database.get_container_client(container)
        
        retry_count = 0
        delay = self.initial_delay
        
        while retry_count <= self.max_retries:
            try:
                document = container_client.read_item(item=key, partition_key=key)
                return document
            except CosmosHttpResponseError as e:
                if e.status_code == 429:
                    if retry_count < self.max_retries:
                        time.sleep(delay)
                        delay = min(delay * 2, self.max_delay)
                        retry_count += 1
                    else:
                        retry_after_ms = e.headers.get('retry-after-ms')
                        if retry_after_ms:
                            time.sleep(int(retry_after_ms) / 1000)
                            try:
                                document = container_client.read_item(item=key, partition_key=key)
                                return document
                            except CosmosHttpResponseError:
                                raise
                        else:
                            raise
                else:
                    raise

    def create_document(self, container, key, body=None) -> dict:
        if not self.database:
            raise ValueError("CosmosDBClient not properly initialized")
        
        container_client = self.database.get_container_client(container)
        
        if body is None:
            body = {}
        
        if 'id' not in body:
            body['id'] = key
        
        retry_count = 0
        delay = self.initial_delay
        
        while retry_count <= self.max_retries:
            try:
                document = container_client.create_item(body=body)
                return document
            except CosmosHttpResponseError as e:
                if e.status_code == 429:
                    if retry_count < self.max_retries:
                        time.sleep(delay)
                        delay = min(delay * 2, self.max_delay)
                        retry_count += 1
                    else:
                        retry_after_ms = e.headers.get('retry-after-ms')
                        if retry_after_ms:
                            time.sleep(int(retry_after_ms) / 1000)
                            try:
                                document = container_client.create_item(body=body)
                                return document
                            except CosmosHttpResponseError:
                                raise
                        else:
                            raise
                else:
                    raise