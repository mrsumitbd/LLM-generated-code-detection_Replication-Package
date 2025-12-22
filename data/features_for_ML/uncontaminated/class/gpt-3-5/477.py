class DebugLevel:

    def __init__(self, level: str | bool):
        self.level = level

    def raise_level(self, other_level: "DebugLevel"):
        if isinstance(other_level, DebugLevel):
            if isinstance(self.level, str) and isinstance(other_level.level, str):
                self.level = other_level.level
            elif isinstance(self.level, bool) and isinstance(other_level.level, bool):
                self.level = other_level.level

    def debug_tools(self):
        if isinstance(self.level, str) and self.level == "tools":
            print("Debugging tools enabled")
        else:
            print("Debugging tools disabled")

    def debug_llm(self):
        if isinstance(self.level, str) and self.level == "llm":
            print("Debugging LLM enabled")
        else:
            print("Debugging LLM disabled")

    def debug_agents(self):
        if isinstance(self.level, str) and self.level == "agents":
            print("Debugging agents enabled")
        else:
            print("Debugging agents disabled")

    def debug_reasoning(self):
        if isinstance(self.level, str) and self.level == "reasoning":
            print("Debugging reasoning enabled")
        else:
            print("Debugging reasoning disabled")

    def debug_all(self):
        if isinstance(self.level, bool) and self.level:
            print("Debugging all enabled")
        else:
            print("Debugging all disabled")

    def is_off(self):
        if isinstance(self.level, bool) and not self.level:
            return True
        else:
            return False

    def __str__(self) -> str:
        return f"DebugLevel: {self.level}"