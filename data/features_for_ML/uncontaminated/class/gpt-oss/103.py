import os
import logging
import fnmatch
from typing import Dict, Optional, List, Tuple


class _LogConfig:
    """Parsed configuration from PYTHON_LOG: default level and per-pattern rules."""

    _LEVEL_MAP = {name: level for level, name in logging._levelToName.items()}

    def __init__(self, env_var: str = "PYTHON_LOG") -> None:
        self._default_level: Optional[int] = None
        self._rules: List[Tuple[str, int]] = []

        raw = os.getenv(env_var)
        if raw:
            self._parse(raw)

    def _parse(self, raw: str) -> None:
        """Parse a comma‑separated list of key=value pairs."""
        for part in raw.split(","):
            part = part.strip()
            if not part:
                continue
            if "=" not in part:
                continue
            key, value = part.split("=", 1)
            key = key.strip()
            value = value.strip()
            level = self._level_from_string(value)
            if level is None:
                continue
            if key.lower() in ("level", "default"):
                self._default_level = level
            else:
                self._rules.append((key, level))

    @staticmethod
    def _level_from_string(name: str) -> Optional[int]:
        """Convert a level name or numeric string to a logging level."""
        if name.isdigit():
            lvl = int(name)
            if lvl in logging._levelToName:
                return lvl
            return None
        return _LogConfig._LEVEL_MAP.get(name.upper())

    @property
    def default_level(self) -> Optional[int]:
        """Return the default logging level (or None if not set)."""
        return self._default_level

    def get_level(self, logger_name: str) -> Optional[int]:
        """
        Return the logging level for the given logger name.

        Rules are evaluated in the order they appear in the configuration.
        The first matching pattern determines the level. If no pattern matches,
        the default level is returned.
        """
        for pattern, level in self._rules:
            if fnmatch.fnmatch(logger_name, pattern):
                return level
        return self._default_level

    def __repr__(self) -> str:
        parts = []
        if self._default_level is not None:
            parts.append(f"default={logging.getLevelName(self._default_level)}")
        for pat, lvl in self._rules:
            parts.append(f"{pat}={logging.getLevelName(lvl)}")
        return f"_LogConfig({', '.join(parts)})"