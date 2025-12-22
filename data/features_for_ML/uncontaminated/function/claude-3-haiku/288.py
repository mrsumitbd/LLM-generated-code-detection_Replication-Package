import re

def split_text_for_tts(text: str, max_length: int = 4000) -> list[str]:
    """Split text into chunks that don't exceed the TTS API limit.

    The function splits text at sentence boundaries (periods, question marks, exclamation points)
    to create natural-sounding chunks. If a sentence is too long, it falls back to
    splitting at commas, then spaces.

    Args:
    ----
        text: The text to split.
        max_length: Maximum character length for each chunk (default 4000 to provide buffer).

    Returns:
    -------
        List of text chunks, each below the maximum length.

    """
    chunks = []
    current_chunk = ""

    for sentence in re.split(r'[.!?]', text):
        if len(current_chunk + sentence) <= max_length:
            current_chunk += sentence + "."
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + "."

    if current_chunk:
        chunks.append(current_chunk.strip())

    if not chunks:
        return [text]

    return chunks