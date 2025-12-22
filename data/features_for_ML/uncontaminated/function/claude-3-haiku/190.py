from typing import Literal
from dataclasses import dataclass

@dataclass
class HTMLOutput:
    layout: str
    content: str

def html(layout: Literal["page", "reflow"]) -> HTMLOutput:
    """HTML output configuration.

    Args:
        layout: The layout type to use for conversion to HTML

    Returns:
        HTMLOutput object
    """
    return HTMLOutput(layout=layout, content="")