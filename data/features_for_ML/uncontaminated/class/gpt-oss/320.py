from __future__ import annotations

from dataclasses import dataclass, field
from contextlib import contextmanager
from typing import List
import copy


@dataclass
class Settings:
    """Simple settings container."""
    debug: bool = False
    log_level: str = "INFO"
    # Add more configuration options here as needed
    # Example:
    # timeout: int = 30
    # retries: int = 3
    # custom_options: dict = field(default_factory=dict)


class GlobalSettings:
    """Manages a global Settings instance with temporary overrides."""

    _stack: List[Settings] = []

    @staticmethod
    def get() -> Settings:
        """Return the current Settings instance."""
        if GlobalSettings._stack:
            return GlobalSettings._stack[-1]
        # Return a default Settings instance if none are set
        return Settings()

    @staticmethod
    @contextmanager
    def push():
        """
        Context manager to temporarily push a copy of the current Settings.
        Any modifications made within the context will be discarded when
        the context exits, restoring the previous Settings.
        """
        current = GlobalSettings.get()
        # Push a deep copy to avoid accidental shared references
        new_settings = copy.deepcopy(current)
        GlobalSettings._stack.append(new_settings)
        try:
            yield new_settings
        finally:
            GlobalSettings._stack.pop()