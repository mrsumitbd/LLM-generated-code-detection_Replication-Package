import os
import time

class CosmosDBClient:
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 5))
    BASE_DELAY = 0.5
    MAX_DELAY = 8

    def __init__(self, config=None):
        self.config = config

    def get_document(self, container, key) -> dict:
        retries = 0
        delay = self.BASE_DELAY
        while retries < self.MAX_RETRIES:
            try:
                # Code to get document from CosmosDB
                return {}  # Placeholder for actual return value
            except Exception as e:
                retries += 1
                if retries == self.MAX_RETRIES:
                    raise e
                time.sleep(delay)
                delay = min(delay * 2, self.MAX_DELAY)

    def create_document(self, container, key, body=None) -> dict:
        retries = 0
        delay = self.BASE_DELAY
        while retries < self.MAX_RETRIES:
            try:
                # Code to create document in CosmosDB
                return {}  # Placeholder for actual return value
            except Exception as e:
                retries += 1
                if retries == self.MAX_RETRIES:
                    raise e
                time.sleep(delay)
                delay = min(delay * 2, self.MAX_DELAY)