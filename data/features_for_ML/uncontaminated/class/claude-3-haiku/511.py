from typing import List

class StructuredTool:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

class AndroidTool:
    def __init__(self):
        self.tools = [
            StructuredTool("Android Studio", "Integrated development environment for Android app development"),
            StructuredTool("Gradle", "Build automation tool for Android projects"),
            StructuredTool("ADB (Android Debug Bridge)", "Command-line tool for communicating with an Android device"),
            StructuredTool("Logcat", "Android's logging system for viewing system debug output"),
            StructuredTool("DDMS (Dalvik Debug Monitor Server)", "Debugging and profiling tool for Android applications")
        ]

    def get_tools(self) -> List[StructuredTool]:
        return self.tools