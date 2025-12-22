def extract_text_blocks(blocks: Iterable[Any] | None) -> str:
    if blocks is None:
        return ''
    
    text_blocks = [str(block) for block in blocks if isinstance(block, str)]
    return ' '.join(text_blocks)