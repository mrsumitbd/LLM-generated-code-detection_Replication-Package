class DebugLevel:

    def __init__(self, level: str | bool):
        if isinstance(level, bool):
            self.level = "all" if level else "off"
        else:
            self.level = level.lower()
        
        self._validate_level()
    
    def _validate_level(self):
        valid_levels = {"off", "tools", "llm", "agents", "reasoning", "all"}
        if self.level not in valid_levels:
            raise ValueError(f"Invalid debug level: {self.level}")
    
    def _get_level_priority(self) -> int:
        priority_map = {
            "off": 0,
            "tools": 1,
            "llm": 2,
            "agents": 3,
            "reasoning": 4,
            "all": 5
        }
        return priority_map.get(self.level, 0)
    
    def raise_level(self, other_level: "DebugLevel"):
        if other_level._get_level_priority() > self._get_level_priority():
            self.level = other_level.level
    
    def debug_tools(self) -> bool:
        return self.level in {"tools", "all"}
    
    def debug_llm(self) -> bool:
        return self.level in {"llm", "all"}
    
    def debug_agents(self) -> bool:
        return self.level in {"agents", "all"}
    
    def debug_reasoning(self) -> bool:
        return self.level in {"reasoning", "all"}
    
    def debug_all(self) -> bool:
        return self.level == "all"
    
    def is_off(self) -> bool:
        return self.level == "off"
    
    def __str__(self) -> str:
        return self.level