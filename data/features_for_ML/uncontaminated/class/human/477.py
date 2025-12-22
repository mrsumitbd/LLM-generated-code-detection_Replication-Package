
class DebugLevel:
    OFF: str = ""

    def __init__(self, level: str | bool):
        if isinstance(level, bool):
            if level == True:
                level = "tools,llm"
            else:
                level = ""
        self.level = str(level)

    def raise_level(self, other_level: "DebugLevel"):
        if self.debug_all():
            return
        if other_level.debug_all():
            self.level = "all"
        elif other_level.level != "":
            self.level = ",".join(set(self.level.split(",")).union(set(other_level.level.split(","))))

    def debug_tools(self):
        return self.level == "all" or "tools" in self.level

    def debug_llm(self):
        return self.level == "all" or "llm" in self.level

    def debug_agents(self):
        return self.level == "all" or "agents" in self.level

    def debug_reasoning(self):
        return "reasoning" in self.level
    
    def debug_all(self):
        return self.level == "all"

    def is_off(self):
        return self.level == ""

    def __str__(self) -> str:
        return str(self.level)