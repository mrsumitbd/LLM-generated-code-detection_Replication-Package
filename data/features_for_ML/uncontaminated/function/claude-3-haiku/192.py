def extract_text_blocks(blocks: Iterable[Any] | None) -> str:
    if blocks is None:
        return ""

    text_blocks = []
    for block in blocks:
        if isinstance(block, str):
            text_blocks.append(block)
        elif hasattr(block, "text"):
            text_blocks.append(block.text)

    return "\n".join(text_blocks)