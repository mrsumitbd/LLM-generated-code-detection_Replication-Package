from typing import List

class StructuredTool:
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version

class AndroidTool:

    def __init__(self):
        self.tools = []

    def get_tools(self) -> List[StructuredTool]:
        return self.tools

# Example usage:
tool1 = StructuredTool("Android Studio", "4.2")
tool2 = StructuredTool("ADB", "1.0")
android_tool = AndroidTool()
android_tool.tools.append(tool1)
android_tool.tools.append(tool2)

for tool in android_tool.get_tools():
    print(f"{tool.name} - Version {tool.version}")