from typing import List
from langchain.tools import StructuredTool

class AndroidTool:
    def __init__(self):
        self.android = Android()

    def get_tools(self) -> List[StructuredTool]:
        return [
            StructuredTool.from_function(
                func=self.android.tap,
                name="tap_screen",
                description="Simulate a tap on the screen at the given coordinates.",
            ),
            StructuredTool.from_function(
                func=self.android.get_screen,
                name="get_screen_content",
                description="Simulate getting the current screen content.",
            ),
            StructuredTool.from_function(
                func=self.android.type_text,
                name="type_text",
                description="Simulate typing text.",
            ),
        ]