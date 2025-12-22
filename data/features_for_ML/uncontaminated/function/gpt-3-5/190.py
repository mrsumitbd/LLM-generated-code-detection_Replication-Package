from typing import Literal

class HTMLOutput:
    def __init__(self, layout: str):
        self.layout = layout

def html(layout: Literal["page", "reflow"]) -> HTMLOutput:
    return HTMLOutput(layout)