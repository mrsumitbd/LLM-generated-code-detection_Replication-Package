import re
from typing import List

def split_text_for_tts(text: str, max_length: int = 4000) -> List[str]:
    """
    Split text into chunks that don't exceed the TTS API limit.

    The function splits text at sentence boundaries (periods, question marks, exclamation points)
    to create natural-sounding chunks. If a sentence is too long, it falls back to
    splitting at commas, then spaces.

    Args:
        text: The text to split.
        max_length: Maximum character length for each chunk (default 4000 to provide buffer).

    Returns:
        List of text chunks, each below the maximum length.
    """
    if not text:
        return []

    # Helper to split a long piece of text into smaller parts
    def _split_long_piece(piece: str) -> List[str]:
        # First try commas
        comma_parts = [p.strip() for p in re.split(r',\s*', piece) if p.strip()]
        sub_chunks = []
        current = ""
        for i, part in enumerate(comma_parts):
            # Add comma back except for the last part
            part_with_comma = part + "," if i < len(comma_parts) - 1 else part
            if len(part_with_comma) <= max_length:
                if len(current) + len(part_with_comma) + (1 if current else 0) <= max_length:
                    current += (" " if current else "") + part_with_comma
                else:
                    if current:
                        sub_chunks.append(current)
                    current = part_with_comma
            else:
                # Split by spaces
                words = part.split()
                word_current = ""
                for word in words:
                    if len(word) > max_length:
                        # Word itself too long; put it alone
                        if word_current:
                            sub_chunks.append(word_current)
                        sub_chunks.append(word)
                        word_current = ""
                        continue
                    if len(word_current) + len(word) + (1 if word_current else 0) <= max_length:
                        word_current += (" " if word_current else "") + word
                    else:
                        if word_current:
                            sub_chunks.append(word_current)
                        word_current = word
                if word_current:
                    if current:
                        if len(current) + len(word_current) + 1 <= max_length:
                            current += " " + word_current
                        else:
                            sub_chunks.append(current)
                            current = word_current
                    else:
                        current = word_current
        if current:
            sub_chunks.append(current)
        return sub_chunks

    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        if len(sentence) <= max_length:
            # Try to add to current chunk
            if len(current_chunk) + len(sentence) + (1 if current_chunk else 0) <= max_length:
                current_chunk += (" " if current_chunk else "") + sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = sentence
        else:
            # Sentence too long; split it
            sub_chunks = _split_long_piece(sentence)
            for sub in sub_chunks:
                if len(current_chunk) + len(sub) + (1 if current_chunk else 0) <= max_length:
                    current_chunk += (" " if current_chunk else "") + sub
                else:
                    if current_chunk:
                        chunks.append(current_chunk)
                    current_chunk = sub

    if current_chunk:
        chunks.append(current_chunk)

    return chunks