from time import time

class CacheEntry:
    
    def __init__(self):
        self._creation_time = time()
    
    @property
    def age(self) -> float:
        return time() - self._creation_time