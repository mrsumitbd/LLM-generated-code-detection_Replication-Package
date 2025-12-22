class DebugLevel:
    DEBUG_LEVELS = {"off": 0, "tools": 1, "llm": 2, "agents": 3, "reasoning": 4, "all": 5}

    def __init__(self, level: str | bool):
        if isinstance(level, str):
            self.level = self.DEBUG_LEVELS.get(level.lower(), 0)
        elif isinstance(level, bool):
            self.level = 5 if level else 0
        else:
            self.level = 0

    def raise_level(self, other_level: "DebugLevel"):
        self.level = max(self.level, other_level.level)

    def debug_tools(self):
        return self.level >= self.DEBUG_LEVELS["tools"]

    def debug_llm(self):
        return self.level >= self.DEBUG_LEVELS["llm"]

    def debug_agents(self):
        return self.level >= self.DEBUG_LEVELS["agents"]

    def debug_reasoning(self):
        return self.level >= self.DEBUG_LEVELS["reasoning"]

    def debug_all(self):
        return self.level >= self.DEBUG_LEVELS["all"]

    def is_off(self):
        return self.level == self.DEBUG_LEVELS["off"]

    def __str__(self) -> str:
        for level, value in self.DEBUG_LEVELS.items():
            if value == self.level:
                return level
        return "unknown"