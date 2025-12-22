from datetime import timedelta
from typing import Any, Dict

class ObjectStore:
    def upload(self, key: str, data: bytes) -> str:
        pass

    def get_presigned_url(self, key: str, expiration: timedelta) -> str:
        pass

class ResourceStore:
    def __init__(self, *, store: ObjectStore, presigned_url_expiration: timedelta = timedelta(days=7)) -> None:
        self.store = store
        self.presigned_url_expiration = presigned_url_expiration
        self.resources: Dict[str, Any] = {}

    def upload(self, key: str, data: bytes) -> str:
        url = self.store.upload(key, data)
        self.resources[key] = {'url': url, 'expiration': self.presigned_url_expiration}
        return url

    def get_presigned_url(self, key: str) -> str:
        if key not in self.resources or self.resources[key]['expiration'] <= timedelta(0):
            url = self.store.get_presigned_url(key, self.presigned_url_expiration)
            self.resources[key] = {'url': url, 'expiration': self.presigned_url_expiration}
        return self.resources[key]['url']