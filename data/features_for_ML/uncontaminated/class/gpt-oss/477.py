class DebugLevel:
    _LEVELS = {
        "off": 0,
        "tools": 1,
        "llm": 2,
        "agents": 3,
        "reasoning": 4,
        "all": 5,
    }

    _LEVEL_NAMES = {v: k for k, v in _LEVELS.items()}

    def __init__(self, level: str | bool):
        if isinstance(level, bool):
            self._level = self._LEVELS["all"] if level else self._LEVELS["off"]
        elif isinstance(level, str):
            key = level.strip().lower()
            if key not in self._LEVELS:
                raise ValueError(f"Invalid debug level: {level!r}")
            self._level = self._LEVELS[key]
        else:
            raise TypeError(f"Level must be str or bool, got {type(level).__name__}")

    def raise_level(self, other_level: "DebugLevel"):
        if not isinstance(other_level, DebugLevel):
            raise TypeError("other_level must be a DebugLevel instance")
        if other_level._level > self._level:
            self._level = other_level._level

    def debug_tools(self) -> bool:
        return self._level >= self._LEVELS["tools"]

    def debug_llm(self) -> bool:
        return self._level >= self._LEVELS["llm"]

    def debug_agents(self) -> bool:
        return self._level >= self._LEVELS["agents"]

    def debug_reasoning(self) -> bool:
        return self._level >= self._LEVELS["reasoning"]

    def debug_all(self) -> bool:
        return self._level == self._LEVELS["all"]

    def is_off(self) -> bool:
        return self._level == self._LEVELS["off"]

    def __str__(self) -> str:
        return self._LEVEL_NAMES[self._level] or "unknown"