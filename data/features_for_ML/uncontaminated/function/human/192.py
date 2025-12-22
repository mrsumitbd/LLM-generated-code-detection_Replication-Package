from collections.abc import Iterable, Sequence
from typing import Any

def extract_text_blocks(blocks: Iterable[Any] | None) -> str:
    pieces: list[str] = []
    for block in blocks or []:
        if isinstance(block, dict):
            block_type = block.get("type")
            if block_type == "text":
                pieces.append(str(block.get("text", "")))
            elif "text" in block:
                pieces.append(str(block.get("text")))
            elif "content" in block:
                pieces.append(extract_text_blocks(block.get("content")))
        elif isinstance(block, str):
            pieces.append(block)
    return "\n".join(piece for piece in pieces if piece)