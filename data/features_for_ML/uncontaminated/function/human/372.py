from typing import Any, Self
from pydantic_ai import BinaryContent

def process_item(item: Any, idx: int | None = None) -> str | float:  # noqa: ANN401
            if isinstance(item, BinaryContent):
                suffix = "" if idx is None else f"_{idx}"
                identifier = f"artifact_{tool_call.tool_call_id}{suffix}"
                artifacts.extend([f"This is {identifier}:", item])
                return f"See {identifier}"
            return item