from contextlib import contextmanager
from typing import Optional

class Settings:
    def __init__(self):
        self.data = {}
    
    def __setitem__(self, key, value):
        self.data[key] = value
    
    def __getitem__(self, key):
        return self.data.get(key)
    
    def __repr__(self):
        return f"Settings({self.data})"
    
    def copy(self):
        new_settings = Settings()
        new_settings.data = self.data.copy()
        return new_settings


class GlobalSettings:
    _current: Optional[Settings] = None
    _stack = []

    @staticmethod
    def get() -> Settings:
        if GlobalSettings._current is None:
            GlobalSettings._current = Settings()
        return GlobalSettings._current

    @staticmethod
    @contextmanager
    def push():
        current = GlobalSettings._current
        GlobalSettings._stack.append(current)
        GlobalSettings._current = GlobalSettings.get().copy() if current else Settings()
        try:
            yield GlobalSettings._current
        finally:
            GlobalSettings._current = GlobalSettings._stack.pop()