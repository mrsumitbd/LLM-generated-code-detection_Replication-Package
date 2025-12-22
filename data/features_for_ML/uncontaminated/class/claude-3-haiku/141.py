import time
from typing import Optional

class RedisLimitAtomicActionCoreMixin:
    """Core mixin for RedisLimitAtomicAction."""

    def __init__(self, backend: "RedisStoreBackend"):
        self.backend = backend
        self.lock_key = f"{self.__class__.__name__}:{self.get_lock_key_suffix()}"
        self.lock_timeout = 60  # 1 minute

    def get_lock_key_suffix(self) -> str:
        raise NotImplementedError

    def acquire_lock(self) -> bool:
        return self.backend.set(self.lock_key, 1, ex=self.lock_timeout, nx=True)

    def release_lock(self) -> bool:
        return self.backend.delete(self.lock_key) == 1

    def execute_with_lock(self, func, *args, **kwargs):
        start_time = time.time()
        while time.time() - start_time < self.lock_timeout:
            if self.acquire_lock():
                try:
                    return func(*args, **kwargs)
                finally:
                    self.release_lock()
            time.sleep(0.1)
        return None

    def execute_with_lock_and_retry(self, func, *args, max_retries: Optional[int] = 3, **kwargs):
        retries = 0
        while retries <= max_retries:
            result = self.execute_with_lock(func, *args, **kwargs)
            if result is not None:
                return result
            retries += 1
        return None