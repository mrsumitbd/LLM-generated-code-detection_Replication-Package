def split_text_for_tts(text: str, max_length: int = 4000) -> list[str]:
    chunks = []
    while len(text) > max_length:
        next_chunk_end = max_length
        for separator in ['.', '?', '!', ',']:
            next_chunk_end = text.rfind(separator, 0, max_length)
            if next_chunk_end != -1:
                break
        if next_chunk_end == -1:
            next_chunk_end = max_length
        chunks.append(text[:next_chunk_end + 1].strip())
        text = text[next_chunk_end + 1:].strip()
    if text:
        chunks.append(text)
    return chunks